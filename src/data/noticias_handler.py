import uuid
from datetime import datetime
from src.models.repository.noticias_repository import NoticiasRepository
from src.http_types.http_request import HttpRequest
from src.http_types.http_response import HttpResponse
from src.errors.errors_type.http_not_found import HttpNotFound

class NoticiaHandler:
    def __init__(self) -> None:
        self.__noticias_repository = NoticiasRepository()

    def register(self, http_request: HttpRequest) -> HttpResponse:
        body = http_request.body

        if "data" in body and body["data"]:
            try:
                body["data"] = datetime.strptime(body["data"], "%d/%m/%Y").date()
            except ValueError:
                try:
                    body["data"] = datetime.strptime(body["data"], "%Y-%m-%d").date()
                except ValueError:
                    body["data"] = datetime.strptime(body["data"], "%d-%m-%Y").date()

        body["uuid"] = str(uuid.uuid4())
        self.__noticias_repository.insert_noticia(body)

        return HttpResponse(
            body={"noticiaId": body["uuid"]},
            status_code=200,
        )

    def find_by_id(self, http_request: HttpRequest) -> HttpResponse:
        noticia_id = http_request.param["noticia_id"]
        noticia = self.__noticias_repository.get_noticia_by_id(noticia_id)

        if not noticia:
            raise HttpNotFound("Notícia não encontrada")

        return HttpResponse(
            body={
                "noticia": {
                    "id": noticia.id,
                    "titulo": noticia.titulo,
                    "descricao": noticia.descricao,
                    "data": noticia.data
                }
            },
            status_code=200,
        )

    def get_all_noticias(self, http_request: HttpRequest) -> HttpResponse:
        noticias = self.__noticias_repository.get_all_noticias()

        return HttpResponse(
            body={
                "noticias": [
                    {
                        "id": noticia.id,
                        "titulo": noticia.titulo,
                        "descricao": noticia.descricao,
                        "data": noticia.data
                    }
                    for noticia in noticias
                ]
            },
            status_code=200,
        )