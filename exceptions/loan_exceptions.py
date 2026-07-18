class LoanLimitExceededException(Exception):

    def __init__(self, user_id):
        super().__init__(f"User with ID {user_id} has reached the loan limit.")
