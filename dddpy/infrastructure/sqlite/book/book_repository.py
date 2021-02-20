from typing import List, Optional

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from dddpy.domain.book.book import Book
from dddpy.domain.book.book_repository import BookRepository
from dddpy.infrastructure.sqlite.book.book_dto import BookDTO, from_entity


class BookRepositoryImpl(BookRepository):
    """BookRepositoryImpl implements of BookRepository to execute CRUD operations with RDBMS."""

    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, book: Book) -> Book:
        book_dto = from_entity(book)
        try:
            self.session.add(book_dto)
        except:
            raise

        return book

    def find_by_isbn(self, isbn: str) -> Optional[Book]:
        try:
            book_dto = self.session.query(BookDTO).filter_by(isbn=isbn).one()
        except NoResultFound:
            return None
        except:
            raise

        return book_dto.to_entity()

    def find_all(
        self,
    ) -> List[Book]:
        try:
            book_dtos = self.session.query(BookDTO).order_by(BookDTO.updated_at).all()
        except:
            raise

        if len(book_dtos) == 0:
            return []

        return list(map(lambda book_dto: book_dto.to_entity(), book_dtos))
