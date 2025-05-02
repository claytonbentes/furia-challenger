from typing import Dict
from src.models.settings.connection import db_connection_handler
from src.models.entities.campeonatos import Campeonatos
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from src.errors.errors_type.http_conflict import HttpConflictError

class CampeonatosRepository:
    def insert_campeonato(self, campeonatoInfo: Dict) -> Dict:
        with db_connection_handler as database:
            try:
                campeonato = Campeonatos(
                    id=campeonatoInfo.get("id"),
                    nome=campeonatoInfo.get("nome"),
                    data_inicio=campeonatoInfo.get("data_inicio"),
                    data_fim=campeonatoInfo.get("data_fim")
                )

                database.session.add(campeonato)
                database.session.commit()

                return campeonatoInfo
            except IntegrityError:
                raise HttpConflictError('Campeonato já cadastrado')

            except Exception as exception:
                database.session.rollback()
                raise exception

    def get_campeonato_by_id(self, campeonato_id: str) -> Campeonatos:
        with db_connection_handler as database:
            try:
                campeonato = (
                    database.session
                    .query(Campeonatos)
                    .filter(Campeonatos.id == campeonato_id)
                    .one()
                )
                return campeonato
            except NoResultFound:
                return None

    def get_all_campeonatos(self) -> list[Campeonatos]:
        with db_connection_handler as database:
            try:
                campeonatos = database.session.query(Campeonatos).all()
                return campeonatos
            except Exception as exception:
                raise exception