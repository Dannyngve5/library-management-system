from unit_of_work.iunit_of_work import IUnitOfWork
from models.user import User
from models.user import UserRole
from exceptions.user_exceptions import UserNotFoundException


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
