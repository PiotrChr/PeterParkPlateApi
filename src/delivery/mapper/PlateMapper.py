from .ResponseMapper import ResponseMapper
from src.infrastructure.model import Plate
from typing import Iterator


class PlateMapper(ResponseMapper):
    def map(self, plates):
        _plates = []
        for plate in plates:
            _plates.append(plate.to_json())

        return _plates
