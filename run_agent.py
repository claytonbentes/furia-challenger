import requests
import json
import re
from typing import Dict, Any, List, Optional

class FuriaQueryAgent:

    """Agente para consultar informações da API FURIA"""

    def __init__(self, base_url: str = "http://localhost:3000"):
        """
        Inicializa o agente com a URL base da API 
        """
        self.base_url = base_url
        self.endpoints = {
            "partidas": "/partidas",
            "proximas_partidas": "/proximas_partidas",
            "noticias": "/noticias",
            "campeonatos": "/campeonatos",
            "players": "/players"
        }
    
    def _make_get_request(self, endpoint: str, resource_id: str = None) -> Dict:
        """
        Faz uma requisição GET a API
        """
        url = f"{self.base_url}{endpoint}"
        if resource_id:
            url = f"{url}/{resource_id}"
            
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Detalhes: {e.response.text}")
            return {"error": str(e)}
    
    # Métodos para identificar o tipo de consulta

    def _is_proximas_partidas_query(self, query: str) -> bool:
        """Verifica se a consulta é sobre próximas partidas"""
        patterns = [
            r'pr(ó|o)xim(a|as|o|os) (partida|partidas|jogo|jogos)',
            r'(partidas|jogos) (futur|pr(ó|o)xim)',
            r'(quando|qual|quais) (ser(á|a)|vai ser|é) (o|a|os|as) pr(ó|o)xim(o|a|os|as)',
            r'agenda(do|dos|da|das)',
            r'calend(a|á)rio (de )?(jogos|partidas)',
            r'(partidas|jogos) (que|para|a) (vir(á|a)|v(ã|a)o acontecer)',
            r'quando (a furia )?(joga|vai jogar)',
            r'(partida|jogo) (seguinte|que vem|depois)',
            r'futuras (partidas|jogos)'
        ]
        return any(re.search(pattern, query) for pattern in patterns)

    def _is_partidas_query(self, query: str) -> bool:
        # Primeiro, verificamos se é uma consulta sobre próximas partidas
        if self._is_proximas_partidas_query(query):
            return False  # Se for sobre próximas partidas, não é sobre partidas passadas
        
        # Padrões para partidas passadas/resultados
        patterns = [
            r'(partidas|jogos|resultados|histórico|confrontos)',
            r'(quais|mostrar|ver|listar) (as )?partidas',
            r'(jogos|partidas) (da )?furia',
            r'vit(ó|o)rias (e|ou) derrotas',
            r'(últimos|recentes|passad(o|os|a|as)) (jogos|resultados|partidas)',
            r'(como foi|qual foi) (o|a) (resultado|placar)',
            r'(partidas|jogos) (anterior|passad)',
            r'histórico (de )?(partidas|jogos|resultados)'
        ]
        return any(re.search(pattern, query) for pattern in patterns)
    
    def _is_noticias_query(self, query: str) -> bool:
        patterns = [
            r'not(í|i)cias',
            r'novidades',
            r'(o que|qual|quais|tem|h(a|á)) (alguma )?not(í|i)cia',
            r'(ultim|últim)(a|as) (informaç(õ|o)es|not(í|i)cias|novidades)',
            r'atualizaç(õ|o)es'
        ]
        return any(re.search(pattern, query) for pattern in patterns)
    
    def _is_campeonatos_query(self, query: str) -> bool:
        patterns = [
            r'campeonat(o|os)',
            r'torneio(s)?',
            r'competiç(ão|ões|ao|oes)',
            r'(quais|listar|mostrar|ver) (os )?campeonatos',
            r'(quais|que) (campeonato|torneio)(s)? (a furia )?(participa|disputa|jogará|jogara|vai jogar|vai participar)'
        ]
        return any(re.search(pattern, query) for pattern in patterns)
    
    def _is_players_query(self, query: str) -> bool:
        patterns = [
            r'jogador(es)?',
            r'player(s)?',
            r'elenco',
            r'time',
            r'equipe',
            r'line(-| )?up',
            r'roster',
            r'quem (são|sao|é|e) (os )?jogadores',
            r'quem (está|esta|joga) (na|no|pela) furia'
        ]
        return any(re.search(pattern, query) for pattern in patterns)
        
    def _get_partidas_data(self, query: str) -> Optional[List[Dict]]:
        response = self._make_get_request(self.endpoints["partidas"])
        if "partidas" in response:
            return response["partidas"]
        return None
    
    def _get_proximas_partidas_data(self, query: str) -> Optional[List[Dict]]:
        response = self._make_get_request(self.endpoints["proximas_partidas"])
        if "proximas_partidas" in response:
            return response["proximas_partidas"]
        return None
    
    def _get_noticias_data(self, query: str) -> Optional[List[Dict]]:
        response = self._make_get_request(self.endpoints["noticias"])
        if "noticias" in response:
            return response["noticias"]
        return None
    
    def _get_campeonatos_data(self, query: str) -> Optional[List[Dict]]:
        response = self._make_get_request(self.endpoints["campeonatos"])
        if "campeonatos" in response:
            return response["campeonatos"]
        return None

    def _get_players_data(self, query: str) -> Optional[List[Dict]]:
        """
        Obtém dados de jogadores da API

        """
        response = self._make_get_request(self.endpoints["players"])
        if "players" in response:
            return response["players"]
        return None
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Processa uma consulta em linguagem natural

        """
        query = query.lower()
        
        response = {
            "found": False,
            "message": "",
            "data": None
        }
        
        if self._is_partidas_query(query):
            data = self._get_partidas_data(query)
            if data:
                response["found"] = True
                response["message"] = "Encontrei as seguintes partidas:"
                response["data"] = data
            else:
                response["message"] = "Não encontrei informações sobre partidas no momento."
        
        elif self._is_proximas_partidas_query(query):
            data = self._get_proximas_partidas_data(query)
            if data:
                response["found"] = True
                response["message"] = "Próximas partidas agendadas:"
                response["data"] = data
            else:
                response["message"] = "Não encontrei informações sobre próximas partidas no momento."
        
        elif self._is_noticias_query(query):
            data = self._get_noticias_data(query)
            if data:
                response["found"] = True
                response["message"] = "Últimas notícias disponíveis:"
                response["data"] = data
            else:
                response["message"] = "Não encontrei notícias no momento."
        
        elif self._is_campeonatos_query(query):
            data = self._get_campeonatos_data(query)
            if data:
                response["found"] = True
                response["message"] = "Informações de campeonatos:"
                response["data"] = data
            else:
                response["message"] = "Não encontrei informações sobre campeonatos no momento."
        
        elif self._is_players_query(query):
            data = self._get_players_data(query)
            if data:
                response["found"] = True
                response["message"] = "Elenco atual da FURIA:"
                response["data"] = data
            else:
                response["message"] = "Não foi possível obter informações sobre o elenco de jogadores no momento."
        
        else:
            response["message"] = "Não entendi o que você está procurando. Por favor, pergunte sobre players, partidas, próximas partidas, notícias ou campeonatos."
            
        return response

if __name__ == "__main__":
    agent = FuriaQueryAgent()
    
    print("=== Teste do Agente FURIA ===")
    print("Digite 'sair' para encerrar\n")
    
    while True:
        # Obter consulta do usuário
        user_query = input("Sua pergunta: ")
        
        if user_query.lower() in ['sair', 'exit', 'quit']:
            print("Encerrando teste do agente.")
            break
        
        # Processar a consulta
        response = agent.process_query(user_query)
        
        # Exibir a resposta
        print("\nResposta: " + response["message"])
        
        # Se encontrou dados, exibir formatados
        if response["found"] and response["data"]:
            print("\nDados encontrados:")
            for i, item in enumerate(response["data"], 1):

                if "adversario" in item and "resultado" in item:
                    data_original = item.get('data', '')
                    data_formatada = data_original
                    
                    if data_original:
                        try:
                            from datetime import datetime
                            
                            if ',' in data_original and any(month in data_original for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
                                import email.utils
                                parsed_date = email.utils.parsedate_to_datetime(data_original)
                                data_formatada = parsed_date.strftime('%d/%m/%Y')
                            elif 'T' in data_original:
                                data_obj = datetime.fromisoformat(data_original.replace('Z', '+00:00'))
                                data_formatada = data_obj.strftime('%d/%m/%Y')
                            elif '-' in data_original and len(data_original) >= 10:
                                data_obj = datetime.strptime(data_original[:10], '%Y-%m-%d')
                                data_formatada = data_obj.strftime('%d/%m/%Y')
                        except Exception:
                            pass
                    
                    print(f"  {i}. vs {item.get('adversario')} - {data_formatada} - {item.get('resultado')} ({item.get('campeonato')})")

                elif "adversario" in item:
                    data_original = item.get('data', '')
                    data_formatada = data_original
                    
                    if data_original:
                        try:
                            from datetime import datetime
                            
                            if ',' in data_original and any(month in data_original for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
                                import email.utils
                                parsed_date = email.utils.parsedate_to_datetime(data_original)
                                data_formatada = parsed_date.strftime('%d/%m/%Y')

                            elif 'T' in data_original:
                                data_obj = datetime.fromisoformat(data_original.replace('Z', '+00:00'))
                                data_formatada = data_obj.strftime('%d/%m/%Y')

                            elif '-' in data_original and len(data_original) >= 10:
                                data_obj = datetime.strptime(data_original[:10], '%Y-%m-%d')
                                data_formatada = data_obj.strftime('%d/%m/%Y')
                        except Exception:
                            pass
                    
                    print(f"  {i}. vs {item.get('adversario')} - {data_formatada} - {item.get('campeonato')}")
                
                elif "titulo" in item:

                    data_original = item.get('data', '')
                    data_formatada = data_original
                    
                    if data_original:
                        try:
                            from datetime import datetime
                            
                            if ',' in data_original and any(month in data_original for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
                                import time
                                import email.utils
                                
                                parsed_date = email.utils.parsedate_to_datetime(data_original)
                                data_formatada = parsed_date.strftime('%d/%m/%Y')
                                
                            elif 'T' in data_original:
                                data_obj = datetime.fromisoformat(data_original.replace('Z', '+00:00'))
                                data_formatada = data_obj.strftime('%d/%m/%Y')
                                
                            elif '-' in data_original and len(data_original) >= 10:
                                data_obj = datetime.strptime(data_original[:10], '%Y-%m-%d')
                                data_formatada = data_obj.strftime('%d/%m/%Y')
                                
                        except Exception as e:
                            pass
                    
                    print(f"  {i}. {item.get('titulo')} ({data_formatada})")
                    
                    if "descricao" in item:
                        desc = item.get('descricao')
                        if len(desc) > 200:
                            desc = desc[:197] + "..."
                        print(f"     {desc}")
                
                elif "nome" in item and "status" in item:
                    campeonato_nome = item.get('nome')
                    campeonato_status = item.get('status')
                    
                    print(f"  {i}. {campeonato_nome} - Status: {campeonato_status}")
                    
                    if "data_inicio" in item and "data_fim" in item:
                        data_inicio = item.get('data_inicio')
                        data_fim = item.get('data_fim')
                        data_inicio_formatada = data_inicio
                        data_fim_formatada = data_fim
                        
                        if data_inicio:
                            try:
                                from datetime import datetime

                                if ',' in data_inicio and any(month in data_inicio for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
                                    import email.utils
                                    parsed_date = email.utils.parsedate_to_datetime(data_inicio)
                                    data_inicio_formatada = parsed_date.strftime('%d/%m/%Y')

                                elif 'T' in data_inicio:
                                    data_obj = datetime.fromisoformat(data_inicio.replace('Z', '+00:00'))
                                    data_inicio_formatada = data_obj.strftime('%d/%m/%Y')

                                elif '-' in data_inicio and len(data_inicio) >= 10:
                                    data_obj = datetime.strptime(data_inicio[:10], '%Y-%m-%d')
                                    data_inicio_formatada = data_obj.strftime('%d/%m/%Y')
                            except Exception:
                                pass
                                
                        if data_fim:
                            try:
                                from datetime import datetime
                                
                                if ',' in data_fim and any(month in data_fim for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
                                    import email.utils
                                    parsed_date = email.utils.parsedate_to_datetime(data_fim)
                                    data_fim_formatada = parsed_date.strftime('%d/%m/%Y')

                                elif 'T' in data_fim:
                                    data_obj = datetime.fromisoformat(data_fim.replace('Z', '+00:00'))
                                    data_fim_formatada = data_obj.strftime('%d/%m/%Y')

                                elif '-' in data_fim and len(data_fim) >= 10:
                                    data_obj = datetime.strptime(data_fim[:10], '%Y-%m-%d')
                                    data_fim_formatada = data_obj.strftime('%d/%m/%Y')
                            except Exception:
                                pass
                        
                        print(f"     De {data_inicio_formatada} até {data_fim_formatada}")
                
                # Melhora a exibição para jogadores
                elif any(key in item for key in ["nome", "nickname", "funcao"]):
                    player_info = []
                    
                    nome = item.get('nome', '')
                    if nome:
                        player_info.append(nome)
                    
                    nickname = item.get('nickname', '')
                    if nickname:
                        if nome:
                            player_info.append(f"'{nickname}'")
                        else:
                            player_info.append(nickname)
                    
                    sobrenome = item.get('sobrenome', '')
                    if sobrenome and sobrenome not in nome:
                        player_info.append(sobrenome)
                    
                    funcao = item.get('funcao', '')
                    if funcao:
                        player_info.append(f"- {funcao}")
                    
                    print(f"  {i}. {' '.join(player_info)}")

                    for key, value in item.items():
                        if key not in ['nome', 'sobrenome', 'nickname', 'funcao', 'id'] and value:
                            formatted_key = key.replace('_', ' ').title()
                            print(f"     {formatted_key}: {value}")
                
                else:
                    formatted_item = {k: v for k, v in item.items() if k != 'id'}
                    print(f"  {i}. {formatted_item}")
        
        print("\n" + "-"*50 + "\n")