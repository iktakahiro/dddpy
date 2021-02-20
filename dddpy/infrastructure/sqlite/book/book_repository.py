from typing import List

from dddpy.domain.book.book import Book
from dddpy.domain.book.book_repository import BookRepository

from .book_dto import BookDTO, from_entity


class BookRepositoryImpl(BookRepository):
    """BookRepositoryImpl implements of BookRepository to execute CRUD operations with RDBMS."""

    def create(self, book: Book):
        book_dto = from_entity(Book)
        print(book_dto)

    def find_by_id(self, id: str) -> Book:
        book_dto = BookDTO()
        return book_dto.to_entity()

    def find_all(
        self,
    ) -> List[Book]:
        book_dto = BookDTO()
        return [book_dto.to_entity()]
