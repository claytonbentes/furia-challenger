from flask import Blueprint, jsonify, request
from src.http_types.http_request import HttpRequest
from src.data.player_handler import PlayerHandler
from src.errors.error_handler import handle_error

player_route_bp = Blueprint("player_route", __name__)

@player_route_bp.route("/players", methods=["POST"])
def create_player():
    try:
        http_request = HttpRequest(body=request.json)
        player_handler = PlayerHandler()

        http_response = player_handler.register(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code

@player_route_bp.route("/players/<player_id>", methods=["GET"])
def get_player(player_id):
    try:

        player_handler = PlayerHandler()
        http_request = HttpRequest(param={"player_id": player_id})
        http_response = player_handler.find_by_id(http_request)

        return jsonify(http_response.body), http_response.status_code

    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code

@player_route_bp.route("/players", methods=["GET"])
def get_players():
    try:
        player_handler = PlayerHandler()
        http_request = HttpRequest()
        http_response = player_handler.get_all_players(http_request)

        return jsonify(http_response.body), http_response.status_code

    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code