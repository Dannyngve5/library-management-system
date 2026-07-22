import unittest

from application.dto.pagination import Pagination
from application.services.library_service import LibraryService


class DummyBooksRepository:
    def __init__(self):
        self.calls = []

    def find_all(self, pagination=None):
        self.calls.append(pagination)
        return ["book"]


class DummyUnitOfWork:
    def __init__(self):
        self.books = DummyBooksRepository()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class LibraryServicePaginationTests(unittest.TestCase):
    def test_find_all_passes_pagination_to_repository(self):
        uow = DummyUnitOfWork()
        service = LibraryService(uow)

        pagination = Pagination(limit=5, offset=10)
        result = service.find_all(pagination=pagination)

        self.assertEqual(result, ["book"])
        self.assertEqual(uow.books.calls[0], pagination)


if __name__ == "__main__":
    unittest.main()
