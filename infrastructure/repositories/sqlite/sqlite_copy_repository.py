from domain.entities.copy import Copy
from application.interfaces.repositories.icopy_repository import ICopyRepository


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
        cursor = self.connection.cursor()

        cursor.execute(
            """
        SELECT *
        FROM copies
        WHERE copy_id = ?
        """,
            (copy_id,),
        )

        row = cursor.fetchone()
        return Copy.from_row(row) if row else None

    def find_all(self) -> list[Copy]:
        cursor = self.connection.cursor()

        cursor.execute("""
        SELECT *
        FROM copies
        """)

        rows = cursor.fetchall()
        return [Copy.from_row(row) for row in rows]

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
        return Copy.from_row(row) if row else None

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

    def delete(self, copy_id: int) -> None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
        DELETE from copies
        WHERE copy_id = ?
        """,
            (copy_id,),
        )

    def delete_by_book_id(self, book_id: int) -> None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
        DELETE FROM copies
        WHERE book_id = ?
        """,
            (book_id,),
        )
