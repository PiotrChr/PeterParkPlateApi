import re

from .exception.MalformedPlateFormatException import MalformedPlateFormatException


class PlateValidator:
    plate_regex = re.compile('^[A-Z]{1,3}-[A-Z]{1,2}[1-9][0-9]{0,3}$')

    def validate(self, plate: str) -> None:
        if not self.plate_regex.fullmatch(plate):
            raise MalformedPlateFormatException('Malformed Plate Format')
