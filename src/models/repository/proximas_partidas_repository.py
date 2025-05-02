from typing import Dict
from src.models.settings.connection import db_connection_handler
from src.models.entities.proximas_partidas import ProximasPartidas
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from src.errors.errors_type.http_conflict import HttpConflictError

class ProximasPartidasRepository:
    def insert_proxima_partida(self, partidaInfo: Dict) -> Dict:
        with db_connection_handler as database:
            try:
                partida = ProximasPartidas(
                    id=partidaInfo.get("id"),
                    data=partidaInfo.get("data"),
                    local=partidaInfo.get("local"),
                    adversario=partidaInfo.get("adversario")
                )

                database.session.add(partida)
                database.session.commit()

                return partidaInfo
            except IntegrityError:
                raise HttpConflictError('Próxima partida já cadastrada')

            except Exception as exception:
                database.session.rollback()
                raise exception

    def get_proxima_partida_by_id(self, partida_id: str) -> ProximasPartidas:
        with db_connection_handler as database:
            try:
                partida = (
                    database.session
                    .query(ProximasPartidas)
                    .filter(ProximasPartidas.id == partida_id)
                    .one()
                )
                return partida
            except NoResultFound:
                return None

    def get_all_proximas_partidas(self) -> list[ProximasPartidas]:
        with db_connection_handler as database:
            try:
                partidas = database.session.query(ProximasPartidas).all()
                return partidas
            except Exception as exception:
                raise exception