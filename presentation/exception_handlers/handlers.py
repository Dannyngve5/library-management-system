from fastapi import Request
from fastapi.responses import JSONResponse

from domain.exceptions.book_exceptions import (
    BookNotFoundException,
    BookHasLoansException,
    DuplicateIsbnException,
)

from domain.exceptions.user_exceptions import (
    UserNotFoundException,
    UserHasLoansException,
)
from domain.exceptions.copy_exceptions import (
    NoAvailableCopiesException,
    CopyNotFoundException,
)
from domain.exceptions.loan_exceptions import (
    LoanLimitExceededException,
    LoanNotFoundException,
    NoActiveLoanException,
)


# Transforma la excepcion de service en una HTTP
def register_exception_handlers(app):

    @app.exception_handler(BookNotFoundException)
    async def book_not_found_handler(request: Request, exc: BookNotFoundException):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(BookHasLoansException)
    async def book_has_loans_handler(request: Request, exc: BookHasLoansException):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(DuplicateIsbnException)
    async def duplicate_isbn_handler(request: Request, exc: DuplicateIsbnException):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(UserNotFoundException)
    async def user_not_found_handler(request: Request, exc: UserNotFoundException):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(LoanLimitExceededException)
    async def loan_limit_exceeded_handler(
        request: Request, exc: LoanLimitExceededException
    ):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(NoAvailableCopiesException)
    async def not_available_copies_handler(
        request: Request, exc: NoAvailableCopiesException
    ):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(UserHasLoansException)
    async def user_has_loans_handler(request: Request, exc: UserHasLoansException):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(LoanNotFoundException)
    async def loan_not_found_handler(request: Request, exc: LoanNotFoundException):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(NoActiveLoanException)
    async def no_active_loan_handler(request: Request, exc: NoActiveLoanException):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(CopyNotFoundException)
    async def copy_not_found_handler(request: Request, exc: CopyNotFoundException):
        return JSONResponse(status_code=404, content={"detail": str(exc)})
