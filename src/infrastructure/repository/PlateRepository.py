from contextlib import AbstractContextManager
from typing import Callable, Iterator
from sqlalchemy.orm import Session
from sqlalchemy import text, select, desc

from src.infrastructure.model.Plate import Plate


class PlateRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> Iterator[Plate]:
        with self.session_factory() as session:
            return session.query(Plate).order_by(desc(Plate.dateCreated)).all()

    def add(self, plate_number: str) -> Plate:
        with self.session_factory() as session:
            plate = Plate(plate_number)
            session.add(plate)

            session.commit()
            session.refresh(plate)

            return plate

    def search_plate(self, key: str, levenshtein: int) -> Iterator[Plate]:
        with self.session_factory() as session:
            query = text(
                "SELECT ID, REPLACE(Plate,'-','') AS Plate, DateCreated FROM tblLicensePlates "
                "WHERE LEVENSHTEIN(:key, Plate) <= :lval "
                "ORDER BY DateCreated DESC"
            )
            orm_sql = select(Plate).from_statement(query)

            result = session.execute(
                orm_sql,
                params={'key': key, 'lval': levenshtein}
            ).all()

            return map(lambda val: val[0], result)
