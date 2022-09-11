from typing import Iterator
from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request, make_response
from flask_expects_json import expects_json
from jsonschema import ValidationError

from src.services.PlateService import PlateService
from src.infrastructure.model.Plate import Plate
from src.di.Container import Container
from src.delivery.mapper.PlateMapper import PlateMapper
from src.delivery.validation.schema import PostPlateSchema
from src.delivery.validation.PlateValidator import PlateValidator
from src.delivery.validation.exception.MalformedPlateFormatException import MalformedPlateFormatException
from src.infrastructure.exception.DuplicateEntityException import DuplicateEntityException

api = Blueprint('api', __name__)


@api.route('/', methods=['GET'])
def index():
    return 'hello', 200


@api.route('/plate', methods=['GET', 'POST'])
@expects_json(PostPlateSchema.schema, ignore_for=['GET'])
@inject
def plate(
        plate_service: PlateService = Provide[Container.plate_service],
        plate_mapper: PlateMapper = Provide[Container.plate_mapper],
        plate_validator: PlateValidator = Provide[Container.plate_validator]
):
    if request.method == 'GET':
        plates: Iterator[Plate] = plate_service.get_all()
        response_data = plate_mapper.map(plates)

        return jsonify(response_data), 200

    if request.method == 'POST':
        plate_number: str = request.json['plate']
        plate_validator.validate(plate_number)

        new_plate = plate_service.add_plate(plate_number)

        return jsonify(new_plate.to_json()), 200


@api.route('/search-plate', methods=['GET'])
def search_plate():
    return 'hello', 200


@api.errorhandler(404)
def resource_not_found(_):
    return make_response(jsonify({'error': 'Resource not found'}), 404)


@api.errorhandler(DuplicateEntityException)
def plate_exists(_):
    return make_response(jsonify({'error': 'Plate already exists'}), 409)


@api.errorhandler(MalformedPlateFormatException)
def malformed_plate_number(_):
    return make_response(jsonify({'error': 'Wrong plate format'}), 422)


@api.errorhandler(ValidationError)
def bad_request(error):
    return make_response(jsonify({'error': error.description.message}), 400)
