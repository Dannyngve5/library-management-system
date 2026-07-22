from abc import ABC, abstractmethod
from domain.entities.user import User


class IUserRepository(ABC):

    @abstractmethod
    def insert(self, user: User) -> User:
        pass

    @abstractmethod
    def find_by_id(self, id_user: int) -> User | None:
        pass

    @abstractmethod
    def find_all(self) -> list[User]:
        pass

    @abstractmethod
    def find_by_role(self, role: str) -> list[User]:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> list[User]:
        pass

    @abstractmethod
    def update(self, user: User) -> None:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass
