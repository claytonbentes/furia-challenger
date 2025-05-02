from typing import Dict
from src.models.settings.connection import db_connection_handler
from src.models.entities.players import Players
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from src.errors.errors_type.http_conflict import HttpConflictError

class PlayersRepository:
    def insert_player(self, playersInfo: Dict) -> Dict:
        with db_connection_handler as database:
            try:
                player = Players(
                    id=playersInfo.get("uuid"),
                    nome=playersInfo.get("nome"),
                    nick=playersInfo.get("nick"),
                    sobrenome=playersInfo.get("sobrenome"),
                    funcao=playersInfo.get("funcao")
            )

                database.session.add(player)
                database.session.commit()

                return playersInfo
            except IntegrityError:
                raise HttpConflictError('Player já cadastrado')

            except Exception as exception:
                database.session.rollback()
                raise exception
    

    def get_player_by_id(self, player_id: str) -> Players:
        with db_connection_handler as database:
            try:
                player = (
                    database.session
                    .query(Players)
                    .filter(Players.id==player_id)
                    .one()
                )
                return player
            
            except NoResultFound:
                return None
    
    def get_all_players(self) -> list[Players]:
        with db_connection_handler as database:
            try:
                players = database.session.query(Players).all()
                return players
            
            except Exception as exception:
                raise exception