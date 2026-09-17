from infrastructure.database.postgres_database import PostgresDatabase

from infrastructure.repositories.postgres.postgres_repository_factory import (
    PostgresRepositoryFactory,
)

from infrastructure.unit_of_work.postgres_unit_of_work import PostgresUnitOfWork

from application.services.library_service import LibraryService
from application.services.user_service import UserService
from application.services.loan_service import LoanService

from config.settings import (
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
)

database = PostgresDatabase(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
)

repository_factory = PostgresRepositoryFactory()

uow = PostgresUnitOfWork(
    database,
    repository_factory,
)

library_service = LibraryService(uow)
user_service = UserService(uow)
loan_service = LoanService(uow)
