from typing import Iterator

from src.infrastructure.model.Plate import Plate
from src.infrastructure.repository.PlateRepository import PlateRepository


class PlateService:
    def __init__(self, plate_repository: PlateRepository):
        self._repository: PlateRepository = plate_repository

    def get_all(self) -> Iterator[Plate]:
        return self._repository.get_all()

    def add_plate(self, plate_number: str) -> Plate:
        return self._repository.add(plate_number)

    def search_plate(self, key, levenshtein: int):
        return self._repository.search_plate(key, levenshtein)
