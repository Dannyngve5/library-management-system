from abc import ABC, abstractmethod

from repositories.interfaces.ibook_repository import IBookRepository
from repositories.interfaces.icopy_repository import ICopyRepository
from repositories.interfaces.iloan_repository import ILoanRepository
from repositories.interfaces.iuser_repository import IUserRepository

# menos util para un proyecto de este tamaño, depende de ella SqliteUniteOfWork, que tiene solo una
# Abstract factory Crear familias de objetos relacionados sin que quien los use sepa cuáles son las clases concretas.
# Sinf factory El UnitOfWork conoce todas las clases concretas.
# Util cuando se tienen varias implementaciones completas de bases de datos,
# ¿El beneficio de añadir una abstracción supera la complejidad que estoy agregando?


class IRepositoryFactory(ABC):

    @abstractmethod
    def create_book_repository(self, connection) -> IBookRepository:
        pass

    @abstractmethod
    def create_copy_repository(self, connection) -> ICopyRepository:
        pass

    @abstractmethod
    def create_user_repository(self, connection) -> IUserRepository:
        pass

    @abstractmethod
    def create_loan_repository(self, connection) -> ILoanRepository:
        pass
