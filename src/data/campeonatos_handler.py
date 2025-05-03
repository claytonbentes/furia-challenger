import uuid
from datetime import datetime
from src.models.repository.campeonatos_repository import CampeonatosRepository
from src.http_types.http_request import HttpRequest
from src.http_types.http_response import HttpResponse
from src.errors.errors_type.http_not_found import HttpNotFound

class CampeonatoHandler:
    def __init__(self) -> None:
        self.__campeonatos_repository = CampeonatosRepository()

    def register(self, http_request: HttpRequest) -> HttpResponse:
        body = http_request.body

        # Converter data_inicio
        if "data_inicio" in body and body["data_inicio"]:
            try:
                body["data_inicio"] = datetime.strptime(body["data_inicio"], "%d/%m/%Y").date()
            except ValueError:
                try:
                    body["data_inicio"] = datetime.strptime(body["data_inicio"], "%Y-%m-%d").date()
                except ValueError:
                    body["data_inicio"] = datetime.strptime(body["data_inicio"], "%d-%m-%Y").date()
        
        # Converter data_fim
        if "data_fim" in body and body["data_fim"]:
            try:
                body["data_fim"] = datetime.strptime(body["data_fim"], "%d/%m/%Y").date()
            except ValueError:
                try:
                    body["data_fim"] = datetime.strptime(body["data_fim"], "%Y-%m-%d").date()
                except ValueError:
                    body["data_fim"] = datetime.strptime(body["data_fim"], "%d-%m-%Y").date()

        body["uuid"] = str(uuid.uuid4())
        self.__campeonatos_repository.insert_campeonato(body)

        return HttpResponse(
            body={"campeonatoId": body["uuid"]},
            status_code=200,
        )

    def find_by_id(self, http_request: HttpRequest) -> HttpResponse:
        campeonato_id = http_request.param["campeonato_id"]
        campeonato = self.__campeonatos_repository.get_campeonato_by_id(campeonato_id)

        if not campeonato:
            raise HttpNotFound("Campeonato não encontrado")

        return HttpResponse(
            body={
                "campeonato": {
                    "id": campeonato.id,
                    "nome": campeonato.nome,
                    "data_inicio": campeonato.data_inicio,
                    "data_fim": campeonato.data_fim,
                    "status": campeonato.status
                }
            },
            status_code=200,
        )

    def get_all_campeonatos(self, http_request: HttpRequest) -> HttpResponse:
        campeonatos = self.__campeonatos_repository.get_all_campeonatos()

        return HttpResponse(
            body={
                "campeonatos": [
                    {
                        "id": campeonato.id,
                        "nome": campeonato.nome,
                        "data_inicio": campeonato.data_inicio,
                        "data_fim": campeonato.data_fim,
                        "status": campeonato.status
                    }
                    for campeonato in campeonatos
                ]
            },
            status_code=200,
        )