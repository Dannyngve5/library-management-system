from datetime import date


class Loan:

    def __init__(
        self,
        loan_id: int | None,
        copy_id: int,
        user_id: int,
        start_date: date,
        due_date: date,
        returned_date: date | None = None,
    ):
        self.loan_id = loan_id
        self.copy_id = copy_id
        self.user_id = user_id
        self.start_date = start_date
        self.due_date = due_date
        self.returned_date = returned_date

    def __str__(self):
        return (
            f"Loan(id={self.loan_id}, "
            f"user_id={self.user_id}, "
            f"copy_id={self.copy_id}, "
            f"start={self.start_date}, "
            f"due={self.due_date}, "
            f"returned={self.returned_date})"
        )

    @classmethod
    def from_row(cls, row):
        return cls(
            loan_id=row[0],
            copy_id=row[1],
            user_id=row[2],
            start_date=row[3],
            due_date=row[4],
            returned_date=row[5],
        )
