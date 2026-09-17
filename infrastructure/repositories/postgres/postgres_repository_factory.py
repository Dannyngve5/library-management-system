from application.interfaces.repositories.irepository_factory import IRepositoryFactory

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


class PostgresRepositoryFactory(IRepositoryFactory):

    def create_book_repository(self, connection):
        return PostgresBookRepository(connection)

    def create_copy_repository(self, connection):
        return PostgresCopyRepository(connection)

    def create_loan_repository(self, connection):
        return PostgresLoanRepository(connection)

    def create_user_repository(self, connection):
        return PostgresUserRepository(connection)
