from __future__ import annotations
from abc import ABC, abstractmethod
from application.interfaces.repositories.ibook_repository import IBookRepository
from application.interfaces.repositories.icopy_repository import ICopyRepository
from application.interfaces.repositories.iuser_repository import IUserRepository
from application.interfaces.repositories.iloan_repository import ILoanRepository


class IUnitOfWork(ABC):

    books: IBookRepository
    copies: ICopyRepository
    loans: ILoanRepository
    users: IUserRepository

    @abstractmethod
    def __enter__(self) -> "IUnitOfWork":
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc, tb):
        pass
