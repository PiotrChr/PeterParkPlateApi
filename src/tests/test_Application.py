from datetime import datetime
from unittest import mock
from flask import url_for
import pytest
import json

from main import create_app
from src.services.PlateService import PlateService
from src.infrastructure.model.Plate import Plate


# /plate [GET]
def test_get_plate(client, app, date_format):
    plate_service_mock = mock.Mock(spec=PlateService)
    plate_service_mock.get_all.return_value = iter(
        [
            Plate('AB-C123', datetime.strptime('2022-01-30 13:55:26', date_format)),
            Plate('A-C1', datetime.strptime('2021-02-28 13:55:26', date_format))
        ]
    )

    with (app.container.plate_service.override(plate_service_mock)):
        response = client.get(url_for("api.get_plate"))

        assert response.status_code == 200
        assert response.data == b'[{"plate":"AB-C123","timestamp":"2022-01-30T13:55:26Z"},' \
                                b'{"plate":"A-C1","timestamp":"2021-02-28T13:55:26Z"}]\n'


# /plate [POST]
def test_post_plate_valid(client, app, valid_plates_request_fixture, headers, sample_date):
    plate_service_mock = mock.Mock(spec=PlateService)

    for valid_request_data, expected_response in valid_plates_request_fixture:
        plate_service_mock.add_plate.return_value = Plate(
            valid_request_data['plate'],
            sample_date
        )

        with (app.container.plate_service.override(plate_service_mock)):
            response = client.post(
                url_for('api.post_plate'),
                data=json.dumps(valid_request_data),
                headers=headers
            )

            assert response.status_code == 200
            assert response.data == expected_response


# /plate [POST]
def test_post_plate_invalid(client, app, invalid_plates_request_fixture, headers):
    plate_service_mock = mock.Mock(spec=PlateService)

    for invalid_request_data, expected_response in invalid_plates_request_fixture:
        with (app.container.plate_service.override(plate_service_mock)):
            response = client.post(
                url_for('api.post_plate'),
                data=json.dumps(invalid_request_data),
                headers=headers
            )

            assert response.status_code == 400
            assert response.data == expected_response


# /plate [POST]
def test_post_plate_malformed_plate(client, app, malformed_plates_request_fixture, headers):
    plate_service_mock = mock.Mock(spec=PlateService)

    for invalid_request_data, expected_response in malformed_plates_request_fixture:
        with (app.container.plate_service.override(plate_service_mock)):
            response = client.post(
                url_for('api.post_plate'),
                data=json.dumps(invalid_request_data),
                headers=headers
            )

            assert response.status_code == 422
            assert response.data == expected_response


# /search-plate [POST]
def test_search_plate(client, app, sample_date):
    plate_service_mock = mock.Mock(spec=PlateService)

    plate_service_mock.search_plate.return_value = iter([Plate('ABC124', sample_date)])

    with (app.container.plate_service.override(plate_service_mock)):
        response = client.get(url_for('api.search_plate', key='ABC123', levenshtein=1))
        # assert response.status_code == 200
        assert response.data == b'{"ABC123":[{"plate":"ABC124","timestamp":"2022-01-30T13:55:26Z"}]}\n'


@pytest.fixture
def app():
    app = create_app()
    yield app
    app.container.unwire()


@pytest.fixture
def headers():
    return {
        'Content-Type': 'application/json',
    }


@pytest.fixture
def date_format():
    return '%Y-%m-%d %H:%M:%S'


@pytest.fixture
def sample_date(date_format):
    return datetime.strptime('2022-01-30 13:55:26', date_format)


@pytest.fixture
def valid_plates_request_fixture():
    return [
        ({'plate': 'VDM-SG98'}, b'{"plate":"VDM-SG98","timestamp":"2022-01-30T13:55:26Z"}\n'),
        ({'plate': 'QA-Y8779'}, b'{"plate":"QA-Y8779","timestamp":"2022-01-30T13:55:26Z"}\n'),
        ({'plate': 'U-R9'}, b'{"plate":"U-R9","timestamp":"2022-01-30T13:55:26Z"}\n'),
        ({'plate': 'E-A8'}, b'{"plate":"E-A8","timestamp":"2022-01-30T13:55:26Z"}\n'),
        ({'plate': 'TK-Z9'}, b'{"plate":"TK-Z9","timestamp":"2022-01-30T13:55:26Z"}\n')
    ]


@pytest.fixture
def invalid_plates_request_fixture():
    return [
        ({'plate': None}, b'{"error":"None is not of type \'string\'"}\n'),
        ({'plte': 'M-PP123'}, b'{"error":"\'plate\' is a required property"}\n'),
        ({}, b'{"error":"\'plate\' is a required property"}\n'),
        (None, b'{"error":"Bad Request"}\n')
    ]


@pytest.fixture
def malformed_plates_request_fixture():
    return [
        ({'plate': 'VDMT-SG98'}, b'{"error":"Wrong plate format"}\n'),
        ({'plate': '-Y8779'}, b'{"error":"Wrong plate format"}\n'),
        ({'plate': 'U-R0'}, b'{"error":"Wrong plate format"}\n'),
        ({'plate': 'E1-A8'}, b'{"error":"Wrong plate format"}\n'),
        ({'plate': 'AV-ZN88888'}, b'{"error":"Wrong plate format"}\n')
    ]


@pytest.fixture
def valid_search_params():
    return [
        (('AB-C123', 1), b'{"error":"Wrong plate format"}\n')
    ]
