from models.book import Book
from models.copy import Copy
from unit_of_work.iunit_of_work import IUnitOfWork
from exceptions.book_exceptions import BookHasLoansException, BookNotFoundException
from dto.book_availability import BookAvailability


class LibraryService:

    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def add_book(self, isbn: str, title: str, author: str, copies: int = 1) -> Book:

        if not isbn.strip():
            raise ValueError("ISBN is required")
        if not title.strip():
            raise ValueError("Title is required")
        if not author.strip():
            raise ValueError("Author is required")
        if copies < 1:
            raise ValueError("Copies  must be greater than 0")

        with self.uow as uow:
            book = Book(isbn, title, author)

            uow.books.insert(book)

            for _ in range(copies):
                uow.copies.insert(Copy(book.book_id))

            return book

    def add_copies(self, book_id: int, copies: int) -> None:
        if copies < 1:
            raise ValueError("Copies  must be greater than 0")

        with self.uow as uow:
            if uow.books.find_by_id(book_id) is None:
                raise BookNotFoundException(book_id)

            for _ in range(copies):
                uow.copies.insert(Copy(book_id))

    def find_books_with_available_copies(self) -> list[BookAvailability]:
        with self.uow as uow:
            return uow.books.find_books_with_available_copies()

    def find_by_isbn(self, isbn: str) -> Book | None:
        if not isbn.strip():
            raise ValueError("ISBN is required")

        with self.uow as uow:
            return uow.books.find_by_isbn(isbn)

    def find_by_id(self, book_id: int) -> Book | None:
        if book_id <= 0:
            raise ValueError("Book ID must be greater than 0")

        with self.uow as uow:
            return uow.books.find_by_id(book_id)

    def find_all(self) -> list[Book]:
        with self.uow as uow:
            return uow.books.find_all()

    def update(self, book_id: int, isbn: str, title: str, author: str) -> None:
        if book_id <= 0:
            raise ValueError("Book ID must be greater than 0")

        if not isbn.strip():
            raise ValueError("ISBN is required")

        if not title.strip():
            raise ValueError("Title is required")

        if not author.strip():
            raise ValueError("Author is required")

        with self.uow as uow:
            book = Book(
                book_id=book_id,
                isbn=isbn,
                title=title,
                author=author,
            )

            uow.books.update(book)

    def delete_book(self, book_id: int):
        with self.uow as uow:
            book = uow.books.find_by_id(book_id)

            if book is None:
                raise BookNotFoundException(book_id)

            if uow.loans.exists_by_book_id(book_id):
                raise BookHasLoansException(book_id)

            uow.copies.delete_by_book_id(book_id)
            uow.books.delete(book_id)
