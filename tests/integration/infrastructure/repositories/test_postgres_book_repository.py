from domain.entities.book import Book

from config.settings import (
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_TEST_HOST,
    POSTGRES_TEST_DB,
    POSTGRES_USER,
)
from infrastructure.database.postgres_database import PostgresDatabase
from infrastructure.repositories.postgres.postgres_book_repository import (
    PostgresBookRepository,
)


def test_insert_and_find_book():

    database = PostgresDatabase(
        host=POSTGRES_TEST_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_TEST_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )

    connection = database.get_connection()

    repository = PostgresBookRepository(connection)

    book = Book(
        book_id=None,
        isbn="9780000000001",
        title="Integration Test Book",
        author="Test Author",
    )

    created_book = repository.insert(book)

    found_book = repository.find_by_id(created_book.book_id)

    assert found_book.book_id == created_book.book_id
    assert found_book.isbn == created_book.isbn
    assert found_book.title == created_book.title
    assert found_book.author == created_book.author

    connection.rollback()
    connection.close()
