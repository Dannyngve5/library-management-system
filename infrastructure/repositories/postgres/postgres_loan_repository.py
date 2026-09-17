from datetime import date

from application.interfaces.repositories.iloan_repository import ILoanRepository
from domain.entities.loan import Loan


class PostgresLoanRepository(ILoanRepository):

    def __init__(self, connection):
        self.connection = connection

    def insert(self, loan: Loan) -> Loan:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO loans(
                copy_id,
                user_id,
                start_date,
                due_date,
                returned_date
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING loan_id
            """,
            (
                loan.copy_id,
                loan.user_id,
                loan.start_date,
                loan.due_date,
                loan.returned_date,
            ),
        )

        loan.loan_id = cursor.fetchone()[0]
        return loan

    def find_active_by_copy(self, copy_id: int) -> Loan | None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM loans
            WHERE copy_id = %s
                AND returned_date IS NULL
            """,
            (copy_id,),
        )

        row = cursor.fetchone()

        return Loan.from_row(row) if row else None

    def find_by_id(self, loan_id: int) -> Loan | None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM loans
            WHERE loan_id = %s
            """,
            (loan_id,),
        )

        row = cursor.fetchone()
        return Loan.from_row(row) if row else None

    def find_by_user(self, user_id: int) -> list[Loan]:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM loans
            WHERE user_id = %s
            """,
            (user_id,),
        )

        rows = cursor.fetchall()
        return [Loan.from_row(row) for row in rows]

    def find_active_by_user(self, user_id: int) -> list[Loan]:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM loans
            WHERE user_id = %s
                AND returned_date IS NULL
            """,
            (user_id,),
        )

        rows = cursor.fetchall()
        return [Loan.from_row(row) for row in rows]

    def find_all(self) -> list[Loan]:
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT *
            FROM loans
            """)

        rows = cursor.fetchall()
        return [Loan.from_row(row) for row in rows]

    def return_book(
        self,
        copy_id: int,
        returned_date: date,
    ) -> None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE loans
            SET returned_date = %s
            WHERE copy_id = %s
                AND returned_date IS NULL
            """,
            (
                returned_date,
                copy_id,
            ),
        )

    def exists_by_book_id(self, book_id: int) -> bool:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM loans l
            JOIN copies c
                ON l.copy_id = c.copy_id
            WHERE c.book_id = %s
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
            WHERE user_id = %s
                AND returned_date IS NULL
            """,
            (user_id,),
        )

        return cursor.fetchone()[0]

    def exists_by_user_id(self, user_id: int) -> bool:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM users
            WHERE user_id = %s
            """,
            (user_id,),
        )

        return cursor.fetchone() is not None
