from typing import Iterator
from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request, make_response
from flask_expects_json import expects_json
from jsonschema import ValidationError
from werkzeug import exceptions

from src.services.PlateService import PlateService
from src.infrastructure.model.Plate import Plate
from src.di.Container import Container
from src.delivery.mapper.PlateMapper import PlateMapper
from src.delivery.validation.schema import PostPlateSchema
from src.delivery.validation.PlateValidator import PlateValidator
from src.delivery.validation.exception.MalformedPlateFormatException import MalformedPlateFormatException

api = Blueprint('api', __name__)


@api.route('/', methods=['GET'])
def index():
    return 'hello', 200


@api.route('/plate', methods=['GET'])
@inject
def get_plate(
        plate_service: PlateService = Provide[Container.plate_service],
        plate_mapper: PlateMapper = Provide[Container.plate_mapper]
):
    plates: Iterator[Plate] = plate_service.get_all()
    response_data = plate_mapper.map(plates)

    return jsonify(response_data), 200


@api.route('/plate', methods=['POST'])
@expects_json(PostPlateSchema.schema)
@inject
def post_plate(
        plate_service: PlateService = Provide[Container.plate_service],
        plate_validator: PlateValidator = Provide[Container.plate_validator]
):
    plate_number: str = request.json['plate']
    plate_validator.validate(plate_number)

    new_plate = plate_service.add_plate(plate_number.upper())

    return jsonify(new_plate.to_json()), 200


@api.route('/search-plate', methods=['GET'])
@inject
def search_plate(
        plate_service: PlateService = Provide[Container.plate_service],
        plate_mapper: PlateMapper = Provide[Container.plate_mapper]
):
    if not request.args.get('key') or not request.args.get('levenshtein'):
        raise ValidationError('Missing required: \'key\' or \'levenshtein\' url param')

    key: str = request.args.get('key')
    levenshtein: int = int(request.args.get('levenshtein')) + 1

    plates: Iterator[Plate] = plate_service.search_plate(key, levenshtein)
    response_data = plate_mapper.map(plates)

    return jsonify({key: response_data}), 200


@api.errorhandler(404)
def resource_not_found(_):
    return make_response(jsonify({'error': 'Resource not found'}), 404)


@api.errorhandler(MalformedPlateFormatException)
def malformed_plate_number(_):
    return make_response(jsonify({'error': 'Wrong plate format'}), 422)


@api.errorhandler(exceptions.BadRequest)
def bad_request(error):
    description = 'Bad Request' if isinstance(error.description, str) else error.description.message
    return make_response(jsonify({'error': description}), 400)
