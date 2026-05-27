from database import get_connection
from datetime import datetime

def calculate_fine(borrow_id):
    """ஒரு specific borrow-க்கு fine எவ்வளவு என்று பார்க்க"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT br.borrow_id, m.name, b.title,
               br.borrow_date, br.due_date,
               br.return_date, br.fine_amount
        FROM borrowings br
        JOIN members m ON br.member_id = m.member_id
        JOIN books b ON br.book_id = b.book_id
        WHERE br.borrow_id = ?
    """, (borrow_id,))
    record = cursor.fetchone()
    conn.close()

    if not record:
        print("❌ Record இல்லை!")
        return

    due = datetime.strptime(record[4], "%Y-%m-%d")
    today = datetime.now()
    overdue_days = max(0, (today - due).days)
    fine = overdue_days * 2  # ஒரு நாளுக்கு ₹2

    print("\n💰 Fine Details:")
    print("-" * 45)
    print(f"Member  : {record[1]}")
    print(f"Book    : {record[2]}")
    print(f"Borrowed: {record[3]}")
    print(f"Due Date: {record[4]}")
    print(f"Overdue : {overdue_days} days")
    print(f"Fine    : ₹{fine}")

def view_all_fines():
    """Fine உள்ள எல்லா records பார்க்க"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.name, b.title, br.due_date,
               br.return_date, br.fine_amount, br.fine_paid
        FROM borrowings br
        JOIN members m ON br.member_id = m.member_id
        JOIN books b ON br.book_id = b.book_id
        WHERE br.fine_amount > 0
    """)
    records = cursor.fetchall()
    conn.close()

    print("\n💰 All Fines:")
    print("-" * 60)
    if records:
        for r in records:
            status = "✅ Paid" if r[5] == 1 else "❌ Unpaid"
            print(f"{r[0]} | {r[1]} | Due:{r[2]} | ₹{r[4]} | {status}")
    else:
        print("Fine எதுவும் இல்லை!")

def pay_fine(borrow_id):
    """Fine கட்டினதும் mark பண்ண"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE borrowings SET fine_paid = 1
        WHERE borrow_id = ? AND fine_amount > 0
    """, (borrow_id,))
    conn.commit()
    conn.close()
    print(f"✅ Fine paid successfully!")

def overdue_report():
    """இன்னும் return பண்ணாத overdue books பார்க்க"""
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT m.name, b.title, br.due_date,
               julianday(?) - julianday(br.due_date) AS overdue_days
        FROM borrowings br
        JOIN members m ON br.member_id = m.member_id
        JOIN books b ON br.book_id = b.book_id
        WHERE br.return_date IS NULL
        AND br.due_date < ?
    """, (today, today))
    records = cursor.fetchall()
    conn.close()

    print("\n⚠️ Overdue Books:")
    print("-" * 55)
    if records:
        for r in records:
            days = int(r[3])
            fine = days * 2
            print(f"{r[0]} | {r[1]} | Due:{r[2]} | {days} days | ₹{fine}")
    else:
        print("Overdue books எதுவும் இல்லை! 🎉")