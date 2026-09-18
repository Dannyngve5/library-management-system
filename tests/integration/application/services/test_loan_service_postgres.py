from domain.entities.book import Book
from domain.entities.copy import Copy
from domain.entities.user import User, UserRole

from application.services.loan_service import LoanService
from config.settings import (
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_TEST_HOST,
    POSTGRES_TEST_DB,
    POSTGRES_USER,
)

from infrastructure.database.postgres_database import PostgresDatabase
from infrastructure.repositories.postgres.postgres_repository_factory import (
    PostgresRepositoryFactory,
)
from infrastructure.unit_of_work.postgres_unit_of_work import PostgresUnitOfWork


def create_database():
    return PostgresDatabase(
        host=POSTGRES_TEST_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_TEST_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )


def test_loan_book_with_postgres(clean_postgres_database):

    database = create_database()
    factory = PostgresRepositoryFactory()

    uow = PostgresUnitOfWork(
        database,
        factory,
    )

    service = LoanService(uow)

    connection = database.get_connection()

    book_repository = factory.create_book_repository(connection)
    user_repository = factory.create_user_repository(connection)
    copy_repository = factory.create_copy_repository(connection)

    book = Book(
        book_id=None,
        isbn="9780000000004",
        title="Loan Service Integration Test",
        author="Test Author",
    )

    user = User(
        user_id=None,
        name="Loan Service Integration User",
        role=UserRole.STUDENT,
    )

    created_book = book_repository.insert(book)
    created_user = user_repository.insert(user)

    copy = Copy(
        copy_id=None,
        book_id=created_book.book_id,
        available=True,
    )

    created_copy = copy_repository.insert(copy)

    connection.commit()
    connection.close()

    loan = service.loan_book(
        created_book.book_id,
        created_user.user_id,
    )

    assert loan.loan_id is not None
    assert loan.copy_id == created_copy.copy_id
    assert loan.user_id == created_user.user_id
    assert loan.returned_date is None

    connection = database.get_connection()

    copy_repository = factory.create_copy_repository(connection)
    loan_repository = factory.create_loan_repository(connection)

    found_copy = copy_repository.find_by_id(created_copy.copy_id)

    found_loan = loan_repository.find_by_id(loan.loan_id)

    assert found_copy.available is False
    assert found_loan.loan_id == loan.loan_id
    assert found_loan.copy_id == created_copy.copy_id
    assert found_loan.user_id == created_user.user_id

    connection.close()


def test_return_book_with_postgres(clean_postgres_database):

    database = create_database()
    factory = PostgresRepositoryFactory()

    uow = PostgresUnitOfWork(
        database,
        factory,
    )

    service = LoanService(uow)

    connection = database.get_connection()

    book_repository = factory.create_book_repository(connection)
    copy_repository = factory.create_copy_repository(connection)
    user_repository = factory.create_user_repository(connection)

    book = Book(
        book_id=None,
        isbn="9780000000005",
        title="Return Book Integration Test",
        author="Test Author",
    )

    user = User(
        user_id=None,
        name="Return Book Integration User",
        role=UserRole.STUDENT,
    )

    created_book = book_repository.insert(book)
    created_user = user_repository.insert(user)

    copy = Copy(
        copy_id=None,
        book_id=created_book.book_id,
        available=True,
    )

    created_copy = copy_repository.insert(copy)

    connection.commit()
    connection.close()

    loan = service.loan_book(
        created_book.book_id,
        created_user.user_id,
    )

    service.return_book(
        created_copy.copy_id,
    )

    connection = database.get_connection()

    copy_repository = factory.create_copy_repository(connection)
    loan_repository = factory.create_loan_repository(connection)

    found_copy = copy_repository.find_by_id(created_copy.copy_id)

    found_loan = loan_repository.find_by_id(loan.loan_id)

    assert found_copy.available is True
    assert found_loan.returned_date is not None

    connection.close()
