from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Plate(Base):
    __tablename__ = "tblLicensePlates"

    id = Column('ID', Integer, primary_key=True)
    plate = Column('Plate', String(10))
    dateCreated = Column('DateCreated', DateTime, server_default=func.now())

    def __init__(self, plate, date_created=None, _id=None):
        self.plate = plate
        self.id = _id
        self.dateCreated = date_created

    def __repr__(self) -> str:
        return f"Plate(id={self.id!r}, plate={self.plate!r}, dateCreated={self.dateCreated!r})"

    def date_iso(self):
        return self.dateCreated.isoformat() + "Z"

    def to_json(self) -> dict:
        return dict(plate=self.plate, timestamp=self.date_iso())
