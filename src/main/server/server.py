from flask import Flask
from flask_cors import CORS
from src.models.settings.connection import db_connection_handler

db_connection_handler.connect_to_db()

app = Flask(__name__)
CORS(app)

from src.main.routes.player_routes import player_route_bp
from src.main.routes.partida_routes import partida_route_bp
from src.main.routes.proxima_partida_routes import proxima_partida_route_bp
from src.main.routes.noticia_routes import noticia_route_bp
from src.main.routes.campeonato_routes import campeonato_route_bp
from src.main.routes.query_routes import query_route_bp


app.register_blueprint(player_route_bp)
app.register_blueprint(partida_route_bp)
app.register_blueprint(proxima_partida_route_bp)
app.register_blueprint(noticia_route_bp)
app.register_blueprint(campeonato_route_bp)
app.register_blueprint(query_route_bp)