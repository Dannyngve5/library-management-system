class Copy:

    def __init__(self, book_id: int, available=True, copy_id: int = None):
        self.copy_id = copy_id
        self.book_id = book_id
        self.available = available

    @classmethod
    def from_row(cls, row):
        return cls(copy_id=row[0], book_id=row[1], available=row[2])
