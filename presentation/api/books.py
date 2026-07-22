from fastapi import APIRouter

from config.dependencies import library_service
from presentation.schemas.book_schema import (
    BookResponse,
    BookCreate,
    BookUpdate,
    BookPatch,
    AvailableBookResponse,
)

router = APIRouter()


@router.post("/books", response_model=BookResponse)
def create_book(book_data: BookCreate) -> BookResponse:
    return library_service.add_book(
        isbn=book_data.isbn, title=book_data.title, author=book_data.author
    )


@router.get("/books", response_model=list[BookResponse])
def get_books() -> list[BookResponse]:
    return library_service.find_all()


@router.get("/books/available", response_model=list[AvailableBookResponse])
def get_books_with_available_copies() -> list[AvailableBookResponse]:
    return library_service.find_books_with_available_copies()


@router.get("/books/{book_id}", response_model=BookResponse)
def get_book_by_id(book_id: int) -> BookResponse:
    return library_service.find_by_id(book_id)


@router.get("/books/isbn/{isbn}", response_model=BookResponse)
def get_book_by_isbn(isbn: str) -> BookResponse:
    return library_service.find_by_isbn(isbn)


@router.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_data: BookUpdate) -> BookResponse:
    return library_service.update(
        book_id=book_id,
        isbn=book_data.isbn,
        title=book_data.title,
        author=book_data.author,
    )


@router.patch("/books/{book_id}", response_model=BookResponse)
def patch_book(book_id: int, book_data: BookPatch) -> BookResponse:
    return library_service.patch(
        book_id,
        book_data.isbn,
        book_data.title,
        book_data.author,
    )


@router.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int) -> None:
    library_service.delete_book(book_id)
