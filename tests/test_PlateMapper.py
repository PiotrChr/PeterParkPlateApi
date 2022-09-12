from unittest import TestCase
import pytest

from src.delivery.mapper.PlateMapper import PlateMapper
from src.infrastructure.model.Plate import Plate


class PlateMapperTest(TestCase):
    def __init__(self):
        self.subject = PlateMapper()
        super().__init__()

    @pytest.fixture
    def mapper_input_fixture(self):
        return [
            (iter([
                Plate('ABC-123'),
                Plate('ABC-124'),
                Plate('ABC-125')
            ]),
             [{'plate': ''}],
             [{'plate': ''}],
             [{'plate': ''}]
            ),
            (iter([
                Plate('ABC-3'),
                Plate('ABC-124'),
                Plate('AC-125')
            ]),
             [{'plate': ''}],
             [{'plate': ''}],
             [{'plate': ''}]
            )
        ]

    def test_map(self, mapper_input_fixture):
        for input_data, expected_output in mapper_input_fixture:
            assert self.subject.map(input_data)
