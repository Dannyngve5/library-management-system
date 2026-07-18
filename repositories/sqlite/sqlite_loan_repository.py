from repositories.interfaces.iloan_repository import ILoanRepository
from models.loan import Loan
import sqlite3


class SqliteLoanRepository(ILoanRepository):

    def __init__(self, connection):
        self.connection = connection

    def insert(self, loan: Loan) -> Loan:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO loans(copy_id, user_id, start_date, due_date, returned_date)
            VALUES (?,?,?,?,?)
            """,
            (
                loan.copy_id,
                loan.user_id,
                loan.start_date,
                loan.due_date,
                loan.returned_date,
            ),
        )

        loan.loan_id = cursor.lastrowid
        return loan

    def find_by_id(self, loan_id: int) -> Loan | None:
        pass

    def find_by_user(self, user_id: int) -> list[Loan]:
        pass

    def find_active_by_user(self, user_id: int) -> list[Loan]:
        pass

    def find_active_by_copy(self, copy_id: int) -> Loan | None:
        pass

    def find_all(self) -> list[Loan]:
        pass

    def update(self, loan: Loan) -> None:
        pass

    def delete(self, loan: Loan) -> None:
        pass

    def exists_by_book_id(self, book_id: int) -> bool:
        cursor = self.connection.cursor()

        cursor.execute(
            """
        SELECT 1
        FROM loans l
        JOIN copies c
            ON l.copy_id= c.copy_id
        WHERE c.book_id = ?
        LIMIT 1
        """,
            (book_id,),
        )
        return cursor.fetchone() is not None

    def count_active_loans_by_user(self, user_id: int) -> int:
        cursor = self.connection.cursor()

        cursor.execute(
            """
        SELECT COUNT(*)
        FROM loans 
        WHERE user_id = ? AND returned_date IS NULL       
        """,
            (user_id,),
        )

        return cursor.fetchone()[0]
