import uuid
from src.models.repository.players_repository import PlayersRepository
from src.http_types.http_request import HttpRequest
from src.http_types.http_response import HttpResponse
from src.errors.errors_type.http_not_found import HttpNotFound

class PlayerHandler:
    def __init__(self) -> None:
        self.__players_repository = PlayersRepository()

    def register(self, http_request: HttpRequest) -> HttpResponse:
        
        body = http_request.body
        body["uuid"] = str(uuid.uuid4())
        self.__players_repository.insert_player(body)

        return HttpResponse(
            body= {"playerId": body["uuid"]},
            status_code=200,
        )

    def find_by_id(self, http_request: HttpRequest) -> HttpResponse:
        player_id = http_request.param["player_id"]
        player = self.__players_repository.get_player_by_id(player_id)

        if not player:
            raise HttpNotFound("Player não encontrado")

        return HttpResponse(
            body={
                "player": {
                    "id": player.id,
                    "nome": player.nome,
                    "nick": player.nick,
                    "sobrenome": player.sobrenome,
                    "funcao": player.funcao
                }
            },
            status_code=200,
        )

    def get_all_players(self, http_request: HttpRequest) -> HttpResponse:
        players = self.__players_repository.get_all_players()

        return HttpResponse(
            body={
                "players": [
                    {
                        "id": player.id,
                        "nome": player.nome,
                        "nick": player.nick,
                        "sobrenome": player.sobrenome,
                        "funcao": player.funcao
                    }
                    for player in players
                ]
            },
            status_code=200,
        )

    def update_player(self, http_request: HttpRequest) -> HttpResponse:
        player_id = http_request.param["player_id"]
        body = http_request.body

        player = self.__players_repository.get_player_by_id(player_id)
        if not player:
            raise HttpNotFound("Player não encontrado")

        # Atualiza os campos do player
        player.nome = body.get("nome", player.nome)
        player.nick = body.get("nick", player.nick)
        player.sobrenome = body.get("sobrenome", player.sobrenome)
        player.funcao = body.get("funcao", player.funcao)

        self.__players_repository.update_player(player)

        return HttpResponse(
            body={"message": "Player atualizado com sucesso"},
            status_code=200,
        )

    def delete_player(self, http_request: HttpRequest) -> HttpResponse:
        player_id = http_request.param["player_id"]

        player = self.__players_repository.get_player_by_id(player_id)
        if not player:
            raise HttpNotFound("Player não encontrado")

        self.__players_repository.delete_player(player_id)

        return HttpResponse(
            body={"message": "Player deletado com sucesso"},
            status_code=200,
        )