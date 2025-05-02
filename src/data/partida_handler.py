import uuid
from src.models.repository.partidas_repository import PartidasRepository
from src.http_types.http_request import HttpRequest
from src.http_types.http_response import HttpResponse
from src.errors.errors_type.http_not_found import HttpNotFound

class PartidaHandler:
    def __init__(self) -> None:
        self.__partidas_repository = PartidasRepository()

    def register(self, http_request: HttpRequest) -> HttpResponse:
        body = http_request.body
        body["uuid"] = str(uuid.uuid4())
        self.__partidas_repository.insert_partida(body)

        return HttpResponse(
            body={"partidaId": body["uuid"]},
            status_code=200,
        )

    def find_by_id(self, http_request: HttpRequest) -> HttpResponse:
        partida_id = http_request.param["partida_id"]
        partida = self.__partidas_repository.get_partida_by_id(partida_id)

        if not partida:
            raise HttpNotFound("Partida não encontrada")

        return HttpResponse(
            body={
                "partida": {
                    "id": partida.id,
                    "adversario": partida.adversario,
                    "data": partida.data,
                    "resultado": partida.resultado,
                    "campeonato": partida.campeonato,
                }
            },
            status_code=200,
        )

    def get_all_partidas(self, http_request: HttpRequest) -> HttpResponse:
        partidas = self.__partidas_repository.get_all_partidas()

        return HttpResponse(
            body={
                "partidas": [
                    {
                        "id": partida.id,
                        "adversario": partida.adversario,
                        "data": partida.data,
                        "resultado": partida.resultado,
                        "campeonato": partida.campeonato,
                    }
                    for partida in partidas
                ]
            },
            status_code=200,
        )