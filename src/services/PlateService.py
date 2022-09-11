from typing import Iterator

from src.infrastructure.model.Plate import Plate
from src.infrastructure.repository.PlateRepository import PlateRepository
from src.infrastructure.exception.DuplicateEntityException import DuplicateEntityException


class PlateService:
    def __init__(self, plate_repository: PlateRepository):
        self._repository: PlateRepository = plate_repository

    def get_all(self) -> Iterator[Plate]:
        return self._repository.get_all()

    def add_plate(self, plate_number: str) -> Plate:
        if self._repository.get_plate_by_number(plate_number):
            raise DuplicateEntityException

        return self._repository.add(plate_number)
