from typing import Dict
from src.models.settings.connection import db_connection_handler
from src.models.entities.proximas_partidas import ProximasPartidas
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from src.errors.errors_type.http_conflict import HttpConflictError

class ProximasPartidasRepository:
    def insert_proxima_partida(self, proximaPartidaInfo: Dict) -> Dict:
        with db_connection_handler as database:
            try:
                proxima_partida = ProximasPartidas(
                    id=proximaPartidaInfo.get("uuid"),
                    adversario=proximaPartidaInfo.get("adversario"),
                    data=proximaPartidaInfo.get("data"),
                    campeonato=proximaPartidaInfo.get("campeonato"),
                    
                )

                database.session.add(proxima_partida)
                database.session.commit()

                return proximaPartidaInfo
            except IntegrityError:
                raise HttpConflictError('Próxima partida já cadastrada')

            except Exception as exception:
                database.session.rollback()
                raise exception

    def get_proxima_partida_by_id(self, proxima_partida_id: str) -> ProximasPartidas:
        with db_connection_handler as database:
            try:
                proxima_partida = (
                    database.session
                    .query(ProximasPartidas)
                    .filter(ProximasPartidas.id == proxima_partida_id)
                    .one()
                )
                return proxima_partida
            except NoResultFound:
                return None

    def get_all_proximas_partidas(self) -> list[ProximasPartidas]:
        with db_connection_handler as database:
            try:
                proxima_partida = database.session.query(ProximasPartidas).all()
                return proxima_partida
            except Exception as exception:
                raise exception