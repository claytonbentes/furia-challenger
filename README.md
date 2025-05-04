# FURIA Chatbot

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

## Descrição

Um agente de IA que funciona como chatbot para responder perguntas sobre o time de CS2 da FURIA Esports. 
Este chatbot utiliza processamento de linguagem natural para entender perguntas sobre a equipe FURIA e fornecer respostas com base em uma API própria criada para este projeto.

O bot pode responder perguntas sobre:

- Players
- Ultimas Partidas
- Próximas partidas
- Notícias
- Campeonatos Recentes

## Uso

### Acesse em: [FURIA Chatbot](https://frontend-liart-ten-88.vercel.app/)

Após iniciar o chatbot, você pode fazer perguntas como preferir relacionadas aos tópicas citados acima.
O agente fará o processamento de linguagem natural e trará as respostas cadastradas na API.

## Estrutura do Projeto

O projeto foi criado seguindo uma arquitetura robusta para possível escalabilidade

- `frontend/` - Frontend feito somente utilizando HTML, CSS, Javascript simples.
- `init/` - SCHEMA Utilizado para criar o banco de dados da API, caso queira criar o banco de dados local.
- `src/` - Código fonte da API
  - `data/` - Gerenciador das funcionalidades da API
  - `errors/` - Erros Personalizados
  - `http_types/` - Gerenciar Requests e Responses da API
  - `main/` - Rotas das API e Servidor Flask.
    - `routes/` - Rotas das API.
    - `server/` - Servidor Flask. 
  - `models/` - Models da API.
    - `entities/` - Entidades da API.
    - `repository/` - Repositories da API.
    - `settings/` - Conexão com banco de dados.
- `.gitignore` - Intruções para o git ignorar arquivos.
- `app.py` - Arquivo principal para rodar a API.
- `requirements.txt` - Bibliotecas usadas para rodar o projeot.
- `run_agent.py` - Arquivo para rodar o Agente de IA.
- `vercel.json` - Configurações da Vercel.


## Melhorias Futuras

- Atualizar a base de conhecimentos da API para ter acesso a um conjunto mais amplo de informações e cadastro de novas rotas de outros assuntos para conseguir responder sobre outros tópicos.
- Implementar inteligência ao Agente de IA para utilizar inteligência artificial para trazer informações não encontradas na API.
- Refatoração de código.


Fique a vontade para clonar o projeto, fazer sugestões, entrar em contato :)

## Contato

[![](https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/claytonbentes/)
[![](https://img.shields.io/badge/-Gmail-%23333?style=for-the-badge&logo=gmail&logoColor=white)](mailto:claytonjhony.bentes@gmail.com)
