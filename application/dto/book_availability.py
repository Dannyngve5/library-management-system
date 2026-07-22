class BookAvailability:

    def __init__(
        self,
        book_id,
        isbn,
        title,
        author,
        available_copies,
    ):
        self.book_id = book_id
        self.isbn = isbn
        self.title = title
        self.author = author
        self.available_copies = available_copies

    @classmethod
    def from_row(cls, row):
        return cls(
            book_id=row[0],
            isbn=row[1],
            title=row[2],
            author=row[3],
            available_copies=row[4],
        )

    def __str__(self):
        return (
            f"Book ID: {self.book_id} | "
            f"ISBN: {self.isbn} | "
            f"Title: {self.title} | "
            f"Author {self.author}"
            f"Available copies {self.available_copies}"
        )
