import psycopg
from psycopg.errors import UniqueViolation

from domain.entities.book import Book
from domain.exceptions.book_exceptions import DuplicateIsbnException
from application.dto.book_availability import BookAvailability
from application.interfaces.repositories.ibook_repository import IBookRepository


class PostgresBookRepository(IBookRepository):

    def __init__(self, connection):
        self.connection = connection

    def insert(self, book: Book) -> Book:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO books(isbn, title, author)
                VALUES (%s, %s, %s)
                RETURNING book_id
                """,
                (
                    book.isbn,
                    book.title,
                    book.author,
                ),
            )

            book.book_id = cursor.fetchone()[0]

        except UniqueViolation:
            raise DuplicateIsbnException(book.isbn)

        return book

    def find_by_isbn(self, isbn: str) -> Book | None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM books
            WHERE isbn = %s
            """,
            (isbn,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return Book.from_row(row)

    def find_by_id(self, book_id: int) -> Book | None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM books
            WHERE book_id = %s
            """,
            (book_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return Book.from_row(row)

    def find_all(self) -> list[Book]:
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT *
            FROM books
            """)

        rows = cursor.fetchall()

        return [Book.from_row(row) for row in rows]

    def find_books_with_available_copies(self) -> list[BookAvailability]:
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT
                b.book_id,
                b.isbn,
                b.title,
                b.author,
                COUNT(c.copy_id) AS available_copies
            FROM books b
            LEFT JOIN copies c
                ON b.book_id = c.book_id
                AND c.available = TRUE
            GROUP BY
                b.book_id,
                b.isbn,
                b.title,
                b.author
            """)

        rows = cursor.fetchall()

        return [BookAvailability.from_row(row) for row in rows]

    def update(self, book: Book) -> None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE books
            SET
                isbn = %s,
                title = %s,
                author = %s
            WHERE book_id = %s
            """,
            (
                book.isbn,
                book.title,
                book.author,
                book.book_id,
            ),
        )

    def delete(self, book_id: int) -> None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            DELETE FROM books
            WHERE book_id = %s
            """,
            (book_id,),
        )
