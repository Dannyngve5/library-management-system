from models.book import Book
from repositories.interfaces.ibook_repository import IBookRepository
from exceptions.book_exceptions import BookNotFoundException, DuplicateIsbnException
from dto.book_availability import BookAvailability
import sqlite3


# Utiliza una conexion, no conoce la clase database
class SqliteBookRepository(IBookRepository):

    def __init__(self, connection):
        self.connection = connection

    # adicionar el libro
    def insert(self, book: Book) -> Book:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO books(isbn, title, author)
                VALUES (?,?,?)
            """,
                (
                    book.isbn,
                    book.title,
                    book.author,
                ),
            )

        except sqlite3.IntegrityError:
            raise DuplicateIsbnException(book.isbn)

        book.book_id = cursor.lastrowid
        return book

    def find_by_isbn(self, isbn: str) -> Book | None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
        SELECT *
        FROM books
        WHERE isbn = ?    
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
        WHERE book_id = ?
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
                AND c.available = 1
            GROUP BY b.book_id, b.isbn, b.title, b.author
            """)

        rows = cursor.fetchall()

        return [BookAvailability.from_row(row) for row in rows]

    def update(self, book: Book) -> None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
        UPDATE books
        SET 
            isbn = ?,
            title = ?,
            author = ?
        WHERE book_id = ?
        """,
            (
                book.isbn,
                book.title,
                book.author,
                book.book_id,
            ),
        )

        if cursor.rowcount == 0:
            raise BookNotFoundException(book.book_id)

    def delete(self, book_id: int) -> None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            DELETE from books
            WHERE book_id = ?
        """,
            (book_id,),
        )

        if cursor.rowcount == 0:
            raise BookNotFoundException(book_id)
