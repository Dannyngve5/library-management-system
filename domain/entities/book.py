class Book:

    def __init__(self, isbn: str, title: str, author: str, book_id: int = None):
        self.book_id = book_id
        self.isbn = isbn
        self.title = title
        self.author = author

    def __str__(self):
        return (
            f"Book ID: {self.book_id} | "
            f"ISBN: {self.isbn} | "
            f"Title: {self.title} | "
            f"Author {self.author}"
        )

    @classmethod
    def from_row(cls, row):
        return cls(book_id=row[0], isbn=row[1], title=row[2], author=row[3])
