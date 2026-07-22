class LoanLimitExceededException(Exception):

    def __init__(self, user_id):
        super().__init__(f"User with ID {user_id} has reached the loan limit.")


class NoActiveLoanException(Exception):
    def __init__(self, copy_id):
        super().__init__(f"Copy with ID {copy_id} does not have an active loan")


class LoanNotFoundException(Exception):
    def __init__(self, loan_id):
        super().__init__(f"Loan with ID {loan_id} not found")
