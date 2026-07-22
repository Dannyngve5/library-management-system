from enum import Enum


class UserRole(Enum):
    STUDENT = "student"
    PROFESSOR = "professor"


class User:

    def __init__(self, name, role: UserRole, user_id: int | None = None):
        self.user_id = user_id
        self.name = name
        self.role = role

    def __str__(self):
        return (
            f"ID: {self.user_id} | " f"Name: {self.name} | " f"Role: {self.role.value}"
        )

    @classmethod
    def from_row(cls, row):
        return cls(
            user_id=row[0],
            name=row[1],
            role=UserRole(row[2]),
        )
