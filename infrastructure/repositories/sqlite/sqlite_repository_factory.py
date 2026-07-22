from application.interfaces.repositories.irepository_factory import IRepositoryFactory
from infrastructure.repositories.sqlite.sqlite_book_repository import (
    SqliteBookRepository,
)
from infrastructure.repositories.sqlite.sqlite_copy_repository import (
    SqliteCopyRepository,
)
from infrastructure.repositories.sqlite.sqlite_loan_repository import (
    SqliteLoanRepository,
)
from infrastructure.repositories.sqlite.sqlite_user_repository import (
    SqliteUserRepository,
)


# Sabe construir todos los repositorios sqlite, si sabe SQL, es mas util en programas grandes donde recibimos varios parametros para armar el objeto
class SqliteRepositoryFactory(IRepositoryFactory):

    def create_book_repository(self, connection):
        return SqliteBookRepository(connection)

    def create_copy_repository(self, connection):
        return SqliteCopyRepository(connection)

    def create_loan_repository(self, connection):
        return SqliteLoanRepository(connection)

    def create_user_repository(self, connection):
        return SqliteUserRepository(connection)
