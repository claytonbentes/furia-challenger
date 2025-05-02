from typing import Dict
from src.models.settings.connection import db_connection_handler
from src.models.entities.noticias import Noticias
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from src.errors.errors_type.http_conflict import HttpConflictError

class NoticiasRepository:
    def insert_noticia(self, noticiaInfo: Dict) -> Dict:
        with db_connection_handler as database:
            try:
                noticia = Noticias(
                    id=noticiaInfo.get("id"),
                    titulo=noticiaInfo.get("titulo"),
                    conteudo=noticiaInfo.get("conteudo"),
                    data_publicacao=noticiaInfo.get("data_publicacao")
                )

                database.session.add(noticia)
                database.session.commit()

                return noticiaInfo
            except IntegrityError:
                raise HttpConflictError('Notícia já cadastrada')

            except Exception as exception:
                database.session.rollback()
                raise exception

    def get_noticia_by_id(self, noticia_id: str) -> Noticias:
        with db_connection_handler as database:
            try:
                noticia = (
                    database.session
                    .query(Noticias)
                    .filter(Noticias.id == noticia_id)
                    .one()
                )
                return noticia
            except NoResultFound:
                return None

    def get_all_noticias(self) -> list[Noticias]:
        with db_connection_handler as database:
            try:
                noticias = database.session.query(Noticias).all()
                return noticias
            except Exception as exception:
                raise exception