import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_connection():
    conn = sqlite3.connect(os.path.join(BASE_DIR, "library.db"))
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT,
            total_copies INTEGER DEFAULT 1,
            available_copies INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            joined_date TEXT DEFAULT CURRENT_DATE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrowings (
            borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            member_id INTEGER,
            borrow_date TEXT DEFAULT CURRENT_DATE,
            due_date TEXT,
            return_date TEXT,
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (member_id) REFERENCES members(member_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fines (
            fine_id INTEGER PRIMARY KEY AUTOINCREMENT,
            borrow_id INTEGER,
            member_id INTEGER,
            fine_amount REAL DEFAULT 0,
            paid INTEGER DEFAULT 0,
            FOREIGN KEY (borrow_id) REFERENCES borrowings(borrow_id),
            FOREIGN KEY (member_id) REFERENCES members(member_id)
        )
    """)

    conn.commit()
    conn.close()