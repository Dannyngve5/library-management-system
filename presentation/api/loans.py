from fastapi import APIRouter

from config.dependencies import loan_service
from presentation.schemas.loan_schema import LoanResponse, LoanCreate

router = APIRouter()


@router.post("/loans", response_model=LoanResponse)
def create_loan(loan_data: LoanCreate) -> LoanResponse:
    return loan_service.loan_book(book_id=loan_data.book_id, user_id=loan_data.user_id)


@router.post("/loans/{copy_id}/return", status_code=204)
def return_copy(copy_id: int) -> None:
    loan_service.return_book(copy_id)


@router.get("/loans", response_model=list[LoanResponse])
def get_loans() -> list[LoanResponse]:
    return loan_service.find_all()


@router.get("/loans/{loan_id}", response_model=LoanResponse)
def get_loan_by_id(loan_id: int) -> LoanResponse:
    return loan_service.find_by_id(loan_id)


@router.get("/loans/user/{user_id}", response_model=list[LoanResponse])
def get_loans_by_user_id(user_id: int) -> list[LoanResponse]:
    return loan_service.find_by_user(user_id)


@router.get("/loans/user/{user_id}/active", response_model=list[LoanResponse])
def get_active_loans_by_user_id(user_id: int) -> list[LoanResponse]:
    return loan_service.find_active_by_user(user_id)
