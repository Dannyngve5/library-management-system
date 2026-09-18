from infrastructure.database.postgres_database import PostgresDatabase
from config.settings import (
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_TEST_HOST,
    POSTGRES_TEST_DB,
    POSTGRES_USER,
)
from infrastructure.repositories.postgres.postgres_repository_factory import (
    PostgresRepositoryFactory,
)
from infrastructure.unit_of_work.postgres_unit_of_work import PostgresUnitOfWork


def test_postgres_unit_of_work():

    database = PostgresDatabase(
        host=POSTGRES_TEST_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_TEST_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )

    factory = PostgresRepositoryFactory()

    uow = PostgresUnitOfWork(
        database,
        factory,
    )

    with uow:
        books = uow.books.find_all()
        copies = uow.copies.find_all()
        users = uow.users.find_all()
        loans = uow.loans.find_all()

    assert books == []
    assert copies == []
    assert users == []
    assert loans == []
