from typing import List, Optional

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from dddpy.usecase.book import BookQueryService, BookReadModel

from .book_dto import BookDTO


class BookQueryServiceImpl(BookQueryService):
    """BookQueryServiceImpl implements READ operations related Book entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_id(self, id: str) -> Optional[BookReadModel]:
        try:
            book_dto = self.session.query(BookDTO).filter_by(id=id).one()
        except NoResultFound:
            return None
        except:
            raise

        return book_dto.to_read_model()

    def find_all(self) -> List[BookReadModel]:
        try:
            book_dtos = (
                self.session.query(BookDTO)
                .order_by(BookDTO.updated_at)
                .limit(100)
                .all()
            )
        except:
            raise

        if len(book_dtos) == 0:
            return []

        return list(map(lambda book_dto: book_dto.to_read_model(), book_dtos))
