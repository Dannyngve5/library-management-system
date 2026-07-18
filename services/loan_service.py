from unit_of_work.iunit_of_work import IUnitOfWork
from datetime import date, timedelta
from exceptions.user_exceptions import UserNotFoundException
from exceptions.book_exceptions import BookNotFoundException
from exceptions.copy_exceptions import NoAvailableCopiesException
from exceptions.loan_exceptions import LoanLimitExceededException
from models.loan import Loan
from models.user import UserRole


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

            if user.role == UserRole.STUDENT:
                limit = 3
            else:
                limit = 10

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

    def return_book():
        pass

    def loan_history():
        pass

    def active_loans():
        pass
