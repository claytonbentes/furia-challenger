import uuid
from datetime import datetime
from src.models.repository.proximas_partidas_repository import ProximasPartidasRepository
from src.http_types.http_request import HttpRequest
from src.http_types.http_response import HttpResponse
from src.errors.errors_type.http_not_found import HttpNotFound

class ProximaPartidaHandler:
    def __init__(self) -> None:
        self.__proximas_partidas_repository = ProximasPartidasRepository()

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
        self.__proximas_partidas_repository.insert_proxima_partida(body)

        return HttpResponse(
            body={"proximaPartidaId": body["uuid"]},
            status_code=200,
        )

    def find_by_id(self, http_request: HttpRequest) -> HttpResponse:
        proxima_partida_id = http_request.param["proxima_partida_id"]
        proxima_partida = self.__proximas_partidas_repository.get_proxima_partida_by_id(proxima_partida_id)

        if not proxima_partida:
            raise HttpNotFound("Proxima Partida não encontrada")

        return HttpResponse(
            body={
                "proxima_partida": {
                    "id": proxima_partida.id,
                    "adversario": proxima_partida.adversario,
                    "data": proxima_partida.data,
                    "campeonato": proxima_partida.campeonato,
                }
            },
            status_code=200,
        )

    def get_all_proximas_partidas(self, http_request: HttpRequest) -> HttpResponse:
        proximas_partidas = self.__proximas_partidas_repository.get_all_proximas_partidas()

        return HttpResponse(
            body={
                "proximas_partidas": [
                    {
                        "id": proxima_partida.id,
                        "adversario": proxima_partida.adversario,
                        "data": proxima_partida.data,
                        "campeonato": proxima_partida.campeonato,
                    }
                    for proxima_partida in proximas_partidas
                ]
            },
            status_code=200,
        )