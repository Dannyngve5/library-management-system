import pytest
from datetime import date, timedelta
from unittest.mock import Mock
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
from domain.entities.user import UserRole


def test_loan_book_success(uow, loan_service, user, book, copy):

    # arrange

    uow.users.find_by_id.return_value = user
    uow.loans.count_active_loans_by_user.return_value = 0
    uow.books.find_by_id.return_value = book
    uow.copies.find_first_available_by_book_id.return_value = copy

    # act

    loan = loan_service.loan_book(book.book_id, user.user_id)

    # assert

    assert loan.copy_id == copy.copy_id
    assert loan.user_id == user.user_id
    assert loan.start_date == date.today()
    assert loan.due_date == date.today() + timedelta(days=15)

    assert copy.available is False
    uow.copies.update.assert_called_once_with(copy)
    uow.loans.insert.assert_called_once_with(loan)


@pytest.mark.parametrize("book_id, user_id", [(0, 1), (10, 0)])
def test_loan_book_invalid_ids(loan_service, book_id, user_id):
    with pytest.raises(ValueError):
        loan_service.loan_book(book_id, user_id)


def test_loan_book_user_not_found(loan_service, uow):
    uow.users.find_by_id.return_value = None

    with pytest.raises(UserNotFoundException):
        loan_service.loan_book(10, 400)


def test_loan_book_book_not_found(loan_service, uow, user):
    uow.books.find_by_id.return_value = None
    uow.users.find_by_id.return_value = user
    uow.loans.count_active_loans_by_user.return_value = 0

    with pytest.raises(BookNotFoundException):
        loan_service.loan_book(12, 5)


@pytest.mark.parametrize(
    "role, active_loans",
    [
        (UserRole.STUDENT, 3),
        (UserRole.PROFESSOR, 10),
    ],
)
def test_loan_book_limit_exceeded(loan_service, uow, user, book, role, active_loans):
    user.role = role
    uow.users.find_by_id.return_value = user
    uow.loans.count_active_loans_by_user.return_value = active_loans

    with pytest.raises(LoanLimitExceededException):
        loan_service.loan_book(book.book_id, user.user_id)


def test_loan_book_no_available_copies(loan_service, uow, user, book):
    uow.books.find_by_id.return_value = book
    uow.users.find_by_id.return_value = user
    uow.loans.count_active_loans_by_user.return_value = 0
    uow.copies.find_first_available_by_book_id.return_value = None

    with pytest.raises(NoAvailableCopiesException):
        loan_service.loan_book(book.book_id, user.user_id)


def test_return_book_invalid_id(loan_service):
    with pytest.raises(ValueError):
        loan_service.return_book(0)


def test_return_book_copy_not_found(loan_service, uow):
    uow.copies.find_by_id.return_value = None

    with pytest.raises(CopyNotFoundException):
        loan_service.return_book(20)


def test_return_book_no_active_loan(loan_service, uow, copy):

    uow.copies.find_by_id.return_value = copy
    uow.loans.find_active_by_copy.return_value = None

    with pytest.raises(NoActiveLoanException):
        loan_service.return_book(copy.copy_id)


def test_return_book_success(loan_service, uow, copy):

    loan = Mock()
    loan.returned_date = None

    uow.copies.find_by_id.return_value = copy
    uow.loans.find_active_by_copy.return_value = loan

    loan_service.return_book(copy.copy_id)

    assert loan.returned_date == date.today()
    assert copy.available is True

    uow.loans.return_book.assert_called_once_with(
        copy.copy_id,
        date.today(),
    )
    uow.copies.update.assert_called_once_with(copy)


def test_find_by_id_invalid_id(loan_service):
    with pytest.raises(ValueError):
        loan_service.find_by_id(0)


def test_find_by_id_not_found(loan_service, uow):
    uow.loans.find_by_id.return_value = None

    with pytest.raises(LoanNotFoundException):
        loan_service.find_by_id(20)


def test_find_by_id_success(loan_service, uow):
    loan = Mock()
    loan.loan_id = 20

    uow.loans.find_by_id.return_value = loan

    result = loan_service.find_by_id(20)

    assert result is loan
    uow.loans.find_by_id.assert_called_once_with(20)


def test_find_by_user_invalid_id(loan_service):
    with pytest.raises(ValueError):
        loan_service.find_by_user(0)


def test_find_by_user_user_not_found(loan_service, uow):
    uow.users.find_by_id.return_value = None

    with pytest.raises(UserNotFoundException):
        loan_service.find_by_user(5)


def test_find_by_user_success(loan_service, uow, user):
    loans = [Mock(), Mock()]

    uow.users.find_by_id.return_value = user
    uow.loans.find_by_user.return_value = loans

    result = loan_service.find_by_user(user.user_id)

    assert result == loans
    uow.users.find_by_id.assert_called_once_with(user.user_id)
    uow.loans.find_by_user.assert_called_once_with(user.user_id)


def test_find_all_success(loan_service, uow):
    loans = [Mock(), Mock(), Mock()]

    uow.loans.find_all.return_value = loans

    result = loan_service.find_all()

    assert result == loans
    uow.loans.find_all.assert_called_once_with()


def test_find_active_by_user_invalid_id(loan_service):
    with pytest.raises(ValueError):
        loan_service.find_active_by_user(0)


def test_find_active_by_user_user_not_found(loan_service, uow):
    uow.users.find_by_id.return_value = None

    with pytest.raises(UserNotFoundException):
        loan_service.find_active_by_user(5)


def test_find_active_by_user_success(loan_service, uow, user):
    loans = [Mock(), Mock()]

    uow.users.find_by_id.return_value = user
    uow.loans.find_active_by_user.return_value = loans

    result = loan_service.find_active_by_user(user.user_id)

    assert result == loans
    uow.users.find_by_id.assert_called_once_with(user.user_id)
    uow.loans.find_active_by_user.assert_called_once_with(user.user_id)
