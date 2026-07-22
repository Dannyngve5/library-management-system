from application.interfaces.iunit_of_work import IUnitOfWork
from datetime import date, timedelta
from domain.exceptions.user_exceptions import UserNotFoundException
from domain.exceptions.book_exceptions import BookNotFoundException
from domain.exceptions.copy_exceptions import (
    NoAvailableCopiesException,
    CopyNotFoundException,
)
from domain.exceptions.loan_exceptions import (
    LoanLimitExceededException,
    NoActiveLoanException,
    LoanNotFoundException,
)
from domain.entities.loan import Loan
from domain.entities.user import UserRole


class LoanService:

    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def loan_book(self, book_id: int, user_id: int) -> Loan:
        if book_id <= 0:
            raise ValueError("Book ID must be positive")
        if user_id <= 0:
            raise ValueError("User ID must be positive")

        with self.uow as uow:

            user = uow.users.find_by_id(user_id)
            if user is None:
                raise UserNotFoundException(user_id)

            active_loans = uow.loans.count_active_loans_by_user(user_id)

            limit = 3 if user.role == UserRole.STUDENT else 10

            if active_loans >= limit:
                raise LoanLimitExceededException(user_id)

            book = uow.books.find_by_id(book_id)
            if book is None:
                raise BookNotFoundException(book_id)

            copy = uow.copies.find_first_available_by_book_id(book_id)
            if copy is None:
                raise NoAvailableCopiesException(book_id)

            loan = Loan(
                None,
                copy.copy_id,
                user.user_id,
                date.today(),
                date.today() + timedelta(days=15),
            )

            copy.available = False
            uow.copies.update(copy)

            uow.loans.insert(loan)

            return loan

    def return_book(self, copy_id: int) -> None:
        if copy_id <= 0:
            raise ValueError("Copy ID must be greater than 0")

        with self.uow as uow:
            copy = uow.copies.find_by_id(copy_id)
            if copy is None:
                raise CopyNotFoundException(copy_id)

            loan = uow.loans.find_active_by_copy(copy_id)
            if loan is None:
                raise NoActiveLoanException(copy_id)

            loan.returned_date = date.today()
            uow.loans.return_book(copy_id, loan.returned_date)

            copy.available = True
            uow.copies.update(copy)

    def find_by_id(self, loan_id: int) -> Loan:
        if loan_id <= 0:
            raise ValueError("Loan ID must be greater than 0")

        with self.uow as uow:
            loan = uow.loans.find_by_id(loan_id)

            if loan is None:
                raise LoanNotFoundException(loan_id)

            return loan

    def find_by_user(self, user_id: int) -> list[Loan]:
        if user_id <= 0:
            raise ValueError("User ID must be greater than 0")

        with self.uow as uow:
            if uow.users.find_by_id(user_id) is None:
                raise UserNotFoundException(user_id)

            return uow.loans.find_by_user(user_id)

    def find_active_by_user(self, user_id: int) -> list[Loan]:
        if user_id <= 0:
            raise ValueError("User ID must be greater than 0")

        with self.uow as uow:
            if uow.users.find_by_id(user_id) is None:
                raise UserNotFoundException(user_id)

            return uow.loans.find_active_by_user(user_id)

    def find_all(self) -> list[Loan]:
        with self.uow as uow:
            return uow.loans.find_all()
