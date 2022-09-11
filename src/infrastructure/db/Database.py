from typing import Callable
from sqlalchemy import create_engine, orm
from sqlalchemy.orm import Session
from contextlib import contextmanager, AbstractContextManager
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Database:
    def __init__(self, db_host: str, db_name: str, db_user: str, db_pass: str) -> None:
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass

        db_url = 'mysql+pymysql://' + self.db_user + ":" + self.db_pass + "@" + self.db_host + "/" + self.db_name

        self._engine = create_engine(db_url, echo=True)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            # Todo: Log something
            session.rollback()
            raise
        finally:
            session.close()
