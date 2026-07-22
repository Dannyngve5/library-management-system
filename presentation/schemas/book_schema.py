from pydantic import BaseModel, ConfigDict


class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    book_id: int
    isbn: str
    title: str
    author: str


class AvailableBookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    book_id: int
    isbn: str
    title: str
    author: str
    available_copies: int


class BookCreate(BaseModel):
    isbn: str
    title: str
    author: str


class BookUpdate(BaseModel):
    isbn: str
    title: str
    author: str


class BookPatch(BaseModel):
    isbn: str | None = None
    title: str | None = None
    author: str | None = None
