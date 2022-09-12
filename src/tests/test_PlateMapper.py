from src.delivery.mapper.PlateMapper import PlateMapper
from src.infrastructure.model.Plate import Plate
from datetime import datetime
import pytest

subject = PlateMapper()


def test_map(mapper_input_data):
    for input_data, expected_output in mapper_input_data:
        assert subject.map(input_data) == expected_output


@pytest.fixture
def mapper_input_data():
    date_format = '%Y-%m-%d %H:%M:%S'

    return [
        (iter([
            Plate('ABC-125', date_created=datetime.strptime('2022-01-30 13:55:26', date_format)),
            Plate('AZ-9', date_created=datetime.strptime('2021-02-28 13:55:26', date_format)),
        ]),
         [
             {'plate': 'ABC-125', 'timestamp': '2022-01-30T13:55:26Z'},
             {'plate': 'AZ-9', 'timestamp': '2021-02-28T13:55:26Z'},
         ]),
        (iter([
            Plate('AAAAA', date_created=datetime.strptime('2022-01-30 13:55:26', date_format)),
            Plate('X', date_created=datetime.strptime('2021-02-28 13:55:26', date_format)),
        ]),
         [
             {'plate': 'AAAAA', 'timestamp': '2022-01-30T13:55:26Z'},
             {'plate': 'X', 'timestamp': '2021-02-28T13:55:26Z'},
         ])
    ]