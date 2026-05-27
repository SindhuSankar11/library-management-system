# -*- coding: utf-8 -*-
from database import create_tables
from library import (add_book, view_all_books, search_book,
                     add_member, view_all_members,
                     borrow_book, return_book)
from fines import calculate_fine, view_all_fines, pay_fine, overdue_report

def main_menu():
    while True:
        print("\n" + "="*45)
        print("     LIBRARY MANAGEMENT SYSTEM")
        print("="*45)
        print("1. Add Book")
        print("2. View All Books")
        print("3. Search Book")
        print("4. Add Member")
        print("5. View All Members")
        print("6. Borrow Book")
        print("7. Return Book")
        print("8. Calculate Fine")
        print("9. View All Fines")
        print("10. Pay Fine")
        print("11. Overdue Report")
        print("0. Exit")
        print("="*45)

        choice = input("Enter choice: ").strip()

        if choice == "1":
            title  = input("Book Title: ").strip()
            author = input("Author: ").strip()
            genre  = input("Genre: ").strip()
            copies = int(input("Copies: ").strip())
            add_book(title, author, genre, copies)

        elif choice == "2":
            view_all_books()

        elif choice == "3":
            keyword = input("Search keyword: ").strip()
            search_book(keyword)

        elif choice == "4":
            name  = input("Member Name: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone: ").strip()
            add_member(name, email, phone)

        elif choice == "5":
            view_all_members()

        elif choice == "6":
            book_id   = int(input("Book ID: ").strip())
            member_id = int(input("Member ID: ").strip())
            borrow_book(book_id, member_id)

        elif choice == "7":
            borrow_id = int(input("Borrow ID: ").strip())
            return_book(borrow_id)

        elif choice == "8":
            borrow_id = int(input("Borrow ID: ").strip())
            calculate_fine(borrow_id)

        elif choice == "9":
            view_all_fines()

        elif choice == "10":
            borrow_id = int(input("Borrow ID: ").strip())
            pay_fine(borrow_id)

        elif choice == "11":
            overdue_report()

        elif choice == "0":
            print("Bye! 👋")
            break

        else:
            print("❌ Wrong choice! Try again.")

if __name__ == "__main__":
    create_tables()
    main_menu()