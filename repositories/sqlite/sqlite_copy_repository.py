from models.copy import Copy
from repositories.interfaces.icopy_repository import ICopyRepository
from exceptions.copy_exceptions import CopyNotFoundException


class SqliteCopyRepository(ICopyRepository):

    def __init__(self, connection):
        self.connection = connection

    def insert(self, copy: Copy) -> Copy:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO copies(book_id, available)
            VALUES (?, ?)
            """,
            (
                copy.book_id,
                copy.available,
            ),
        )

        copy.copy_id = cursor.lastrowid
        return copy

    def find_by_id(self, copy_id: int) -> Copy | None:
        pass

    def find_all(self) -> list[Copy]:
        pass

    def find_first_available_by_book_id(self, book_id: int) -> Copy | None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
        SELECT *
        FROM copies
        WHERE book_id = ? AND available = 1
        LIMIT 1
        """,
            (book_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return Copy.from_row(row)

    def update(self, copy: Copy) -> None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE copies
            SET available = ?
            WHERE copy_id = ?
            """,
            (
                copy.available,
                copy.copy_id,
            ),
        )

        if cursor.rowcount == 0:
            raise CopyNotFoundException(copy.copy_id)

    def delete(self, copy: Copy) -> None:
        pass

    def delete_by_book_id(self, book_id: int) -> None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
        DELETE FROM copies
        WHERE book_id = ?
        """,
            (book_id,),
        )
