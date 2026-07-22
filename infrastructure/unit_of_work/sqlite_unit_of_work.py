from infrastructure.database.database import Database
from application.interfaces.iunit_of_work import IUnitOfWork
from application.interfaces.repositories.irepository_factory import IRepositoryFactory


# Administra la conexión
# Recibe Database Factory de BookRepository  Factory de CopyRepository
class SqliteUnitOfWork(IUnitOfWork):

    def __init__(self, database: Database, repository_factory: IRepositoryFactory):
        self.database = database
        self.repository_factory = repository_factory

    def __enter__(self):
        self.connection = self.database.get_connection()  # Abre la conexion

        self.books = self.repository_factory.create_book_repository(
            self.connection
        )  # No conoce SQL está desacomplado - INYECCION DE DEPENDENCIAS

        self.copies = self.repository_factory.create_copy_repository(self.connection)

        self.users = self.repository_factory.create_user_repository(self.connection)

        self.loans = self.repository_factory.create_loan_repository(self.connection)

        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type:
            self.connection.rollback()
        else:
            self.connection.commit()

        self.connection.close()
