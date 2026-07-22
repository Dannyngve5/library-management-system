from infrastructure.database.database import Database
from infrastructure.repositories.sqlite.sqlite_repository_factory import (
    SqliteRepositoryFactory,
)
from infrastructure.unit_of_work.sqlite_unit_of_work import SqliteUnitOfWork

from application.services.library_service import LibraryService
from application.services.user_service import UserService
from application.services.loan_service import LoanService

database = Database("library.db")

repository_factory = SqliteRepositoryFactory()

uow = SqliteUnitOfWork(database, repository_factory)

library_service = LibraryService(uow)
user_service = UserService(uow)
loan_service = LoanService(uow)
