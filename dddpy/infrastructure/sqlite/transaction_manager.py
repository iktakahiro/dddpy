from sqlalchemy.orm.session import Session

from dddpy.infrastructure.sqlite.book.book_repository import (
    BookRepository,
    BookRepositoryImpl,
)
from dddpy.usecase.transaction_manager import TransactionManager


class SqlAlchemyTransactionManager(TransactionManager):
    def __init__(self, session: Session):
        self.session = session

    def __enter__(self):
        self.book_repository: BookRepository = BookRepositoryImpl(session=self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
