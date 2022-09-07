from flask import Flask, Blueprint, Response, jsonify, request

api = Blueprint('api', __name__)


@api.route('/')
def index():
    return 'hello', 200


@api.route('/plate', methods=['GET', 'POST'])
def plate():
    return 'hello', 200


@api.route('/search-plate', methods=['GET', 'POST'])
def search_plate():
    return 'hello', 200


@api.errorhandler(404)
def resource_not_found():
    return jsonify({"error": "Resource not found"}), 404
