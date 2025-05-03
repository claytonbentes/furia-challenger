from flask import Blueprint, jsonify, request
from src.http_types.http_request import HttpRequest
from src.data.proximas_partidas_handler import ProximaPartidaHandler
from src.errors.error_handler import handle_error

proxima_partida_route_bp = Blueprint("proxima_partida_route", __name__)

@proxima_partida_route_bp.route("/proximas_partidas", methods=["POST"])
def create_proxima_partida():
    try:
        http_request = HttpRequest(body=request.json)
        proxima_partida_handler = ProximaPartidaHandler()

        http_response = proxima_partida_handler.register(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code

@proxima_partida_route_bp.route("/proximas_partidas/<proxima_partida_id>", methods=["GET"])
def get_proxima_partida(proxima_partida_id):
    try:

        proxima_partida_handler = ProximaPartidaHandler()
        http_request = HttpRequest(param={"proxima_partida_id": proxima_partida_id})
        http_response = proxima_partida_handler.find_by_id(http_request)

        return jsonify(http_response.body), http_response.status_code

    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code

@proxima_partida_route_bp.route("/proximas_partidas", methods=["GET"])
def get_proximas_partidas():
    try:
        proximas_partidas = ProximaPartidaHandler()
        http_request = HttpRequest()
        http_response = proximas_partidas.get_all_proximas_partidas(http_request)

        return jsonify(http_response.body), http_response.status_code

    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code