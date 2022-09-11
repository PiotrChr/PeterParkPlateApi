from contextlib import AbstractContextManager
from typing import Callable, Iterator
from sqlalchemy.orm import Session

from src.infrastructure.model.Plate import Plate


class PlateRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> Iterator[Plate]:
        with self.session_factory() as session:
            return session.query(Plate).all()

    def get_plate_by_number(self, plate_number: str):
        with self.session_factory() as session:
            return session.query(Plate).filter_by(plate=plate_number).first()

    def add(self, plate_number: str) -> Plate:
        with self.session_factory() as session:
            plate = Plate(plate_number)
            session.add(plate)

            session.commit()
            session.refresh(plate)

            return plate
