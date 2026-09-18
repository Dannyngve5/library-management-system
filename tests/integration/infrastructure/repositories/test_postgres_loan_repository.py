from datetime import date

from domain.entities.book import Book
from domain.entities.copy import Copy
from domain.entities.loan import Loan
from domain.entities.user import User, UserRole

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
from infrastructure.repositories.postgres.postgres_copy_repository import (
    PostgresCopyRepository,
)
from infrastructure.repositories.postgres.postgres_loan_repository import (
    PostgresLoanRepository,
)
from infrastructure.repositories.postgres.postgres_user_repository import (
    PostgresUserRepository,
)


def test_insert_and_find_loan():

    database = PostgresDatabase(
        host=POSTGRES_TEST_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_TEST_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )

    connection = database.get_connection()

    book_repository = PostgresBookRepository(connection)
    copy_repository = PostgresCopyRepository(connection)
    user_repository = PostgresUserRepository(connection)
    loan_repository = PostgresLoanRepository(connection)

    book = Book(
        book_id=None,
        isbn="9780000000003",
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

    user = User(
        user_id=None,
        name="Integration Test User",
        role=UserRole.STUDENT,
    )

    created_user = user_repository.insert(user)

    loan = Loan(
        loan_id=None,
        copy_id=created_copy.copy_id,
        user_id=created_user.user_id,
        start_date=date(2026, 9, 17),
        due_date=date(2026, 10, 2),
        returned_date=None,
    )

    created_loan = loan_repository.insert(loan)

    found_loan = loan_repository.find_by_id(created_loan.loan_id)

    assert found_loan.loan_id == created_loan.loan_id
    assert found_loan.copy_id == created_loan.copy_id
    assert found_loan.user_id == created_loan.user_id
    assert found_loan.start_date == created_loan.start_date
    assert found_loan.due_date == created_loan.due_date
    assert found_loan.returned_date == created_loan.returned_date

    connection.rollback()
    connection.close()
