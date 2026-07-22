class NoAvailableCopiesException(Exception):

    def __init__(self, book_id):
        super().__init__(f"Book with ID {book_id} has no available copies")


class CopyNotFoundException(Exception):

    def __init__(self, copy_id):
        super().__init__(f"Copy with ID {copy_id} not found")
