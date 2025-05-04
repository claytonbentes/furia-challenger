import sys
import os
from run_agent import FuriaQueryAgent
from flask import Blueprint, request, jsonify

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

agent = FuriaQueryAgent()

query_route_bp = Blueprint("query_route", __name__)

@query_route_bp.route('/query', methods=['POST'])
def process_query():
    """
    Endpoint para processar consultas do frontend.
    """
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"found": False, "message": "Consulta inválida. Envie um campo 'query'."}), 400

    query = data['query']
    response = agent.process_query(query)

    if isinstance(response, dict) and 'message' in response:
        return jsonify(response)
    else:
        return jsonify({"found": False, "message": "Erro ao processar a consulta.", "data": None})