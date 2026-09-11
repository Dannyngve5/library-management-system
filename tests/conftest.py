import pytest
from unittest.mock import MagicMock, Mock
from application.services.loan_service import LoanService
from domain.entities.user import UserRole


@pytest.fixture
def uow():
    uow = MagicMock()
    uow.__enter__.return_value = uow
    return uow


@pytest.fixture
def loan_service(uow):
    return LoanService(uow)


@pytest.fixture
def user():
    user = Mock()
    user.user_id = 5
    user.role = UserRole.STUDENT
    return user


@pytest.fixture
def book():
    book = Mock()
    book.book_id = 10
    return book


@pytest.fixture
def copy():
    copy = Mock()
    copy.copy_id = 20
    copy.available = False
    return copy
