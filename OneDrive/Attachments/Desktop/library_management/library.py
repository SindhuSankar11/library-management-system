from database import get_connection
from datetime import datetime, timedelta

def add_book(title, author, genre, copies):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO books (title, author, genre, total_copies, available_copies)
        VALUES (?, ?, ?, ?, ?)
    """, (title, author, genre, copies, copies))
    conn.commit()
    conn.close()
    print(f"✅ '{title}' book successfully add ஆச்சு!")

def search_book(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT book_id, title, author, genre, available_copies
        FROM books
        WHERE title LIKE ? OR author LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))
    results = cursor.fetchall()
    conn.close()
    if results:
        print(f"\n📚 Search Results:")
        print("-" * 55)
        for row in results:
            print(f"ID:{row[0]} | {row[1]} | {row[2]} | {row[3]} | Available:{row[4]}")
    else:
        print(f"❌ '{keyword}' என்ற book இல்லை!")

def view_all_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT book_id, title, author, genre, available_copies FROM books")
    books = cursor.fetchall()
    conn.close()
    print("\n📚 All Books:")
    print("-" * 55)
    if books:
        for book in books:
            print(f"ID:{book[0]} | {book[1]} | {book[2]} | {book[3]} | Available:{book[4]}")
    else:
        print("இன்னும் எந்த book-உம் add ஆகவில்லை!")

def add_member(name, email, phone):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO members (name, email, phone)
            VALUES (?, ?, ?)
        """, (name, email, phone))
        conn.commit()
        print(f"✅ '{name}' member successfully add ஆச்சு!")
    except:
        print(f"❌ இந்த email already registered!")
    conn.close()

def view_all_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT member_id, name, email, phone FROM members")
    members = cursor.fetchall()
    conn.close()
    print("\n👥 All Members:")
    print("-" * 55)
    if members:
        for m in members:
            print(f"ID:{m[0]} | {m[1]} | {m[2]} | {m[3]}")
    else:
        print("இன்னும் எந்த member-உம் add ஆகவில்லை!")

def borrow_book(book_id, member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT available_copies, title FROM books WHERE book_id=?", (book_id,))
    book = cursor.fetchone()
    if not book:
        print("❌ Book இல்லை!")
        conn.close()
        return
    if book[0] <= 0:
        print(f"❌ '{book[1]}' இப்போது available இல்லை!")
        conn.close()
        return
    due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    cursor.execute("""
        INSERT INTO borrowings (book_id, member_id, due_date)
        VALUES (?, ?, ?)
    """, (book_id, member_id, due_date))
    cursor.execute("""
        UPDATE books SET available_copies = available_copies - 1
        WHERE book_id = ?
    """, (book_id,))
    conn.commit()
    conn.close()
    print(f"✅ Book borrowed! Due date: {due_date}")

def return_book(borrow_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.title, br.due_date, br.return_date, br.book_id
        FROM borrowings br
        JOIN books b ON br.book_id = b.book_id
        WHERE br.borrow_id = ?
    """, (borrow_id,))
    record = cursor.fetchone()
    if not record:
        print("❌ Borrow record இல்லை!")
        conn.close()
        return
    if record[2]:
        print("❌ இந்த book ஏற்கனவே return ஆச்சு!")
        conn.close()
        return
    today = datetime.now().strftime("%Y-%m-%d")
    due = datetime.strptime(record[1], "%Y-%m-%d")
    diff = (datetime.now() - due).days
    fine = max(0, diff) * 2
    cursor.execute("""
        UPDATE borrowings SET return_date = ?, fine_amount = ?
        WHERE borrow_id = ?
    """, (today, fine, borrow_id))
    cursor.execute("""
        UPDATE books SET available_copies = available_copies + 1
        WHERE book_id = ?
    """, (record[3],))
    conn.commit()
    conn.close()
    if fine > 0:
        print(f"✅ Book returned! Fine: ₹{fine}")
    else:
        print(f"✅ Book returned on time! No fine.")