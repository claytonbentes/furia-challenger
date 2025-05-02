from flask import Blueprint, jsonify, request
from src.http_types.http_request import HttpRequest
from src.data.campeonatos_handler import CampeonatoHandler
from src.errors.error_handler import handle_error

campeonato_route_bp = Blueprint("campeonato_route", __name__)

@campeonato_route_bp.route("/campeonatos", methods=["POST"])
def create_campeonato():
    try:
        http_request = HttpRequest(body=request.json)
        campeonato_handler = CampeonatoHandler()

        http_response = campeonato_handler.register(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code

@campeonato_route_bp.route("/campeonatos/<campeonato_id>", methods=["GET"])
def get_campeonato(campeonato_id):
    try:

        campeonato_handler = CampeonatoHandler()
        http_request = HttpRequest(param={"campeonato_id": campeonato_id})
        http_response = campeonato_handler.find_by_id(http_request)

        return jsonify(http_response.body), http_response.status_code

    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code

@campeonato_route_bp.route("/campeonatos", methods=["GET"])
def get_campeonatos():
    try:
        campeonato_handler = CampeonatoHandler()
        http_request = HttpRequest()
        http_response = campeonato_handler.get_all_campeonatos(http_request)

        return jsonify(http_response.body), http_response.status_code

    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code