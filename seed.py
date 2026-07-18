from models.book import Book
from models.copy import Copy
from models.user import User, UserRole
from models.loan import Loan
from datetime import date, timedelta


def seed_database(uow):

    with uow as uow:

        # ======================
        # USERS
        # ======================

        users = [
            User("Daniel", UserRole.STUDENT),
            User("Laura", UserRole.STUDENT),
            User("Carlos", UserRole.STUDENT),
            User("Maria", UserRole.PROFESSOR),
            User("Andres", UserRole.PROFESSOR),
        ]

        for user in users:
            uow.users.insert(user)

        # ======================
        # BOOKS + COPIES
        # ======================

        books = [
            ("9780132350884", "Clean Code", "Robert C. Martin", 2),
            ("9781491950357", "Python Crash Course", "Eric Matthes", 2),
            ("9780201616224", "The Pragmatic Programmer", "Andrew Hunt", 2),
            ("9780134685991", "Effective Java", "Joshua Bloch", 1),
            ("9780134757599", "Refactoring", "Martin Fowler", 1),
            ("9780262033848", "Introduction to Algorithms", "Cormen", 1),
            ("9781617294433", "Grokking Algorithms", "Aditya Bhargava", 1),
            ("9780596007126", "Head First Design Patterns", "Eric Freeman", 1),
            ("9780135957059", "Artificial Intelligence", "Russell", 1),
            ("9780596009205", "Learning Python", "Mark Lutz", 1),
        ]

        created_copies = []

        for isbn, title, author, copies in books:

            book = Book(isbn=isbn, title=title, author=author)

            uow.books.insert(book)

            for _ in range(copies):
                copy = Copy(book.book_id)

                uow.copies.insert(copy)

                created_copies.append(copy)

        # ======================
        # LOANS
        # ======================

        loan1 = Loan(
            None,
            created_copies[0].copy_id,  # Clean Code copia 1
            users[0].user_id,  # Daniel
            date.today() - timedelta(days=10),
            date.today() + timedelta(days=5),
            None,
        )

        uow.loans.insert(loan1)

        created_copies[0].available = False
        uow.copies.update(created_copies[0])

        loan2 = Loan(
            None,
            created_copies[2].copy_id,  # Python Crash Course copia 1
            users[1].user_id,  # Laura
            date.today() - timedelta(days=5),
            date.today() + timedelta(days=10),
            None,
        )

        uow.loans.insert(loan2)

        created_copies[2].available = False
        uow.copies.update(created_copies[2])
