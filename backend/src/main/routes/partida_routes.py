from flask import Blueprint, jsonify, request
from src.http_types.http_request import HttpRequest
from src.data.partida_handler import PartidaHandler
from src.errors.error_handler import handle_error

partida_route_bp = Blueprint("partida_route", __name__)

@partida_route_bp.route("/partidas", methods=["POST"])
def create_partida():
    try:
        http_request = HttpRequest(body=request.json)
        partida_handler = PartidaHandler()

        http_response = partida_handler.register(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code

@partida_route_bp.route("/partidas/<partida_id>", methods=["GET"])
def get_partida(partida_id):
    try:

        partida_handler = PartidaHandler()
        http_request = HttpRequest(param={"partida_id": partida_id})
        http_response = partida_handler.find_by_id(http_request)

        return jsonify(http_response.body), http_response.status_code

    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code

@partida_route_bp.route("/partidas", methods=["GET"])
def get_partidas():
    try:
        partida_handler = PartidaHandler()
        http_request = HttpRequest()
        http_response = partida_handler.get_all_partidas(http_request)

        return jsonify(http_response.body), http_response.status_code

    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code