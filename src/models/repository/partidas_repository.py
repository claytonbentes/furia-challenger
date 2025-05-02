from typing import Dict
from src.models.settings.connection import db_connection_handler
from src.models.entities.partidas import Partidas
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from src.errors.errors_type.http_conflict import HttpConflictError

class PartidasRepository:
    def insert_partida(self, partidaInfo: Dict) -> Dict:
        with db_connection_handler as database:
            try:
                partida = Partidas(
                    id=partidaInfo.get("id"),
                    data=partidaInfo.get("data"),
                    local=partidaInfo.get("local"),
                    time_casa=partidaInfo.get("time_casa"),
                    time_visitante=partidaInfo.get("time_visitante")
                )

                database.session.add(partida)
                database.session.commit()

                return partidaInfo
            except IntegrityError:
                raise HttpConflictError('Partida já cadastrada')

            except Exception as exception:
                database.session.rollback()
                raise exception

    def get_partida_by_id(self, partida_id: str) -> Partidas:
        with db_connection_handler as database:
            try:
                partida = (
                    database.session
                    .query(Partidas)
                    .filter(Partidas.id == partida_id)
                    .one()
                )
                return partida
            except NoResultFound:
                return None

    def get_all_partidas(self) -> list[Partidas]:
        with db_connection_handler as database:
            try:
                partidas = database.session.query(Partidas).all()
                return partidas
            except Exception as exception:
                raise exception