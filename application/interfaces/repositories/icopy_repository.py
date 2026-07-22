from abc import ABC, abstractmethod
from domain.entities.copy import Copy


class ICopyRepository(ABC):

    @abstractmethod
    def insert(self, copy: Copy) -> Copy:
        pass

    @abstractmethod
    def find_by_id(self, copy_id: int) -> Copy | None:
        pass

    @abstractmethod
    def find_all(self) -> list[Copy]:
        pass

    @abstractmethod
    def update(self, copy: Copy) -> None:
        pass

    @abstractmethod
    def delete(self, copy_id: int) -> None:
        pass

    @abstractmethod
    def find_first_available_by_book_id(self, book_id: int) -> Copy | None:
        pass

    @abstractmethod
    def delete_by_book_id(self, book_id: int) -> None:
        pass
