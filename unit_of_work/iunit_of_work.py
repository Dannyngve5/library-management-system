from __future__ import annotations
from abc import ABC, abstractmethod
from repositories.interfaces.ibook_repository import IBookRepository
from repositories.interfaces.icopy_repository import ICopyRepository
from repositories.interfaces.iuser_repository import IUserRepository
from repositories.interfaces.iloan_repository import ILoanRepository


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
