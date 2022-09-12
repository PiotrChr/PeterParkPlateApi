import pytest

from src.delivery.validation.PlateValidator import PlateValidator
from src.delivery.validation.exception.MalformedPlateFormatException import MalformedPlateFormatException

subject = PlateValidator()


def test_validator_positive(valid_plates_fixture):
    for plate_number in valid_plates_fixture:
        assert subject.validate(plate_number) is None


def test_validator_negative(invalid_plates_fixture):
    for plate_number in invalid_plates_fixture:
        with pytest.raises(MalformedPlateFormatException):
            subject.validate(plate_number)


@pytest.fixture
def valid_plates_fixture():
    return [
        'VDM-SG98',
        'QA-Y8779',
        'U-R9',
        'AV-ZN8',
        'K-K97',
        'QYJ-HK9529',
        'E-A8',
        'J-W798',
        'JW-R89',
        'TK-Z9'
    ]


@pytest.fixture
def invalid_plates_fixture():
    return [
        'VDMT-SG98',
        '-Y8779',
        'U-R0',
        'AV-ZN88888',
        'K-KAA97',
        '123-HK9529',
        'E1-A8',
        '1J1-W798',
        '00-000',
        'TK-Z09'
    ]
