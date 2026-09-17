from domain.entities.book import Book
from domain.entities.copy import Copy

from config.settings import (
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_TEST_DB,
    POSTGRES_USER,
)
from infrastructure.database.postgres_database import PostgresDatabase
from infrastructure.repositories.postgres.postgres_book_repository import (
    PostgresBookRepository,
)
from infrastructure.repositories.postgres.postgres_copy_repository import (
    PostgresCopyRepository,
)


def test_insert_and_find_copy():

    database = PostgresDatabase(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_TEST_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )

    connection = database.get_connection()

    book_repository = PostgresBookRepository(connection)
    copy_repository = PostgresCopyRepository(connection)

    book = Book(
        book_id=None,
        isbn="9780000000002",
        title="Integration Test Book",
        author="Test Author",
    )

    created_book = book_repository.insert(book)

    copy = Copy(
        copy_id=None,
        book_id=created_book.book_id,
        available=True,
    )

    created_copy = copy_repository.insert(copy)

    found_copy = copy_repository.find_by_id(created_copy.copy_id)

    assert found_copy.copy_id == created_copy.copy_id
    assert found_copy.book_id == created_copy.book_id
    assert found_copy.available == created_copy.available

    connection.rollback()
    connection.close()
