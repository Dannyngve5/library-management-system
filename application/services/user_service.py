from application.interfaces.iunit_of_work import IUnitOfWork
from domain.entities.user import User
from domain.entities.user import UserRole
from domain.exceptions.user_exceptions import (
    UserNotFoundException,
    UserHasLoansException,
)


class UserService:

    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def add_user(self, name: str, role: str):

        if not name.strip():
            raise ValueError("Name is required")

        try:
            role = UserRole(role.lower())
        except ValueError:
            raise ValueError("Invalid role")

        with self.uow as uow:

            user = User(name, role)
            uow.users.insert(user)

            return user

    def find_by_id(self, user_id: int) -> User:
        if user_id <= 0:
            raise ValueError("User ID must be greatter than 0")

        with self.uow as uow:
            user = uow.users.find_by_id(user_id)

            if user is None:
                raise UserNotFoundException(user_id)

            return user

    def find_all(self) -> list[User]:
        with self.uow as uow:
            return uow.users.find_all()

    def find_by_role(self, role: str) -> list[User]:
        try:
            role = UserRole(role.lower())
        except ValueError:
            raise ValueError("Invalid role")

        with self.uow as uow:
            return uow.users.find_by_role(role)

    def patch(self, user_id: int, name: str | None, role: str | None) -> User:
        if user_id <= 0:
            raise ValueError("User ID must be greater than 0")

        with self.uow as uow:
            user = uow.users.find_by_id(user_id)

            if not user:
                raise UserNotFoundException(user_id)

            if name is not None:
                if not name.strip():
                    raise ValueError("Name is required")
                user.name = name

            if role is not None:
                if not role.strip():
                    raise ValueError("Role is required")
                try:
                    role = UserRole(role.lower())
                except ValueError:
                    raise ValueError("Invalid role")
                user.role = role

            uow.users.update(user)
            return user

    def delete(self, user_id: int) -> None:
        if user_id <= 0:
            raise ValueError("User ID must be greatter than 0")

        with self.uow as uow:
            user = uow.users.find_by_id(user_id)

            if not user:
                raise UserNotFoundException(user_id)

            if uow.loans.exists_by_user_id(user_id):
                raise UserHasLoansException(user_id)

            uow.users.delete(user_id)
