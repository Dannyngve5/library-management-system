from abc import ABC, abstractmethod
from domain.entities.book import Book
from application.dto.book_availability import BookAvailability


# servicio no debería conocer detalles de infraestructura. Interfaz 1. desacopla dependencias (pruebas, separar responsabilidades, evolucion) 2. define un contrato
# evita que el servicio conozca persistencia
class IBookRepository(ABC):

    @abstractmethod
    def insert(self, book: Book) -> Book:
        pass

    @abstractmethod
    def find_by_isbn(self, isbn: str) -> Book | None:
        pass

    @abstractmethod
    def find_by_id(self, book_id: int) -> Book | None:
        pass

    @abstractmethod
    def find_all(self) -> list[Book]:
        pass

    @abstractmethod
    def find_books_with_available_copies(self) -> list[BookAvailability]:
        pass

    @abstractmethod
    def update(self, book: Book) -> None:
        pass

    @abstractmethod
    def delete(self, book_id: int) -> None:
        pass
