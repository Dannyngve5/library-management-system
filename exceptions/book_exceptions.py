class BookNotFoundException(Exception):

    def __init__(self, book_id: int):
        super().__init__(f"Book with id {book_id} was not found")


class BookHasLoansException(Exception):
    def __init__(self, book_id):
        super().__init__(
            f"Book with id {book_id} has loan history and cannot be deleted"
        )


class DuplicateIsbnException(Exception):
    def __init__(self, isbn: str):
        super().__init__(f"Book with ISBN {isbn} already exists")
