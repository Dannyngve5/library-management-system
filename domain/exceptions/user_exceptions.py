class UserNotFoundException(Exception):

    def __init__(self, user_id: int):
        super().__init__(f"User with id {user_id} was not found")


class UserHasLoansException(Exception):

    def __init__(self, user_id):
        super().__init__(
            "User with id {user_id} has loan history and cannot be deleted"
        )
