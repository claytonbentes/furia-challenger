from flask import Blueprint, jsonify, request
from src.http_types.http_request import HttpRequest
from src.data.noticias_handler import NoticiasHandler
from src.errors.error_handler import handle_error

noticia_route_bp = Blueprint("noticia_route", __name__)

@noticia_route_bp.route("/noticias", methods=["POST"])
def create_noticia():
    try:
        http_request = HttpRequest(body=request.json)
        noticia_handler = NoticiaHandler()

        http_response = noticia_handler.register(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code

@noticia_route_bp.route("/noticias/<noticia_id>", methods=["GET"])
def get_noticia(noticia_id):
    try:

        noticia_handler = NoticiaHandler()
        http_request = HttpRequest(param={"noticia_id": noticia_id})
        http_response = noticia_handler.find_by_id(http_request)

        return jsonify(http_response.body), http_response.status_code

    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code

@noticia_route_bp.route("/noticias", methods=["GET"])
def get_noticias():
    try:
        noticia_handler = NoticiaHandler()
        http_request = HttpRequest()
        http_response = noticia_handler.get_all_noticias(http_request)

        return jsonify(http_response.body), http_response.status_code

    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code