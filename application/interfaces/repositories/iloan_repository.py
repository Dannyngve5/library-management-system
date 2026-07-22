from abc import ABC, abstractmethod
from domain.entities.loan import Loan
from datetime import date


class ILoanRepository(ABC):

    @abstractmethod
    def insert(self, loan: Loan) -> Loan:
        pass

    @abstractmethod
    def find_by_id(self, loan_id: int) -> Loan | None:
        pass

    @abstractmethod
    def find_by_user(self, user_id: int) -> list[Loan]:
        pass

    @abstractmethod
    def find_active_by_user(self, user_id: int) -> list[Loan]:
        pass

    @abstractmethod
    def find_active_by_copy(self, copy_id: int) -> Loan | None:
        pass

    @abstractmethod
    def return_book(self, copy_id: int, returned_date: date) -> None:
        pass

    @abstractmethod
    def find_all(self) -> list[Loan]:
        pass

    @abstractmethod
    def exists_by_book_id(self, book_id: int) -> bool:
        pass

    @abstractmethod
    def count_active_loans_by_user(self, user_id: int) -> int:
        pass

    @abstractmethod
    def exists_by_user_id(self, user_id: int) -> bool:
        pass
