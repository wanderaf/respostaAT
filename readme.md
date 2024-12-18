Descrição e Objetivo
Este projeto consiste em uma aplicação para análise de partidas de futebol, oferecendo funcionalidades como:

Sumarização de partidas: Resumo textual dos principais eventos da partida.
Perfil de jogador: Estatísticas detalhadas de jogadores em partidas específicas.
Narração personalizada: Geração de textos narrativos com estilos variados.
A aplicação possui duas abordagens:

FastAPI: Uma API para acesso programático às funcionalidades.
Streamlit: Uma interface interativa para explorar os dados de forma visual.


Configuração do Ambiente
Clone o repositório:

git clone https://github.com/wanderaf/dtat/tree/main/OneDrive/INFNET/7.%206%C2%BA%20Semestre/Desenvolvimento%20de%20Data-Driven%20Apps%20com%20Python/AT
cd seu-repositorio
Crie o ambiente virtual:

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
Instale as dependências:

pip install -r requirements.txt
Inicie os serviços:

FastAPI:
uvicorn app.fastapi_app:app --reload

Streamlit:
streamlit run app.streamlit_app.py
Exemplos de Entrada e Saída
Endpoint: /match_summary
Entrada:

{
  "match_id": 3788741
}

Saída:
{
  "summary": "O time A venceu o time B por 3 a 1. Destaques: gols de João e Lucas, assistência de Ana."
}

Endpoint: /player_profile
Entrada:

{
  "match_id": 3788741,
  "player_name": "Lionel Messi"
}
Saída:

{
  "player_profile": {
    "Passes": 45,
    "Finalizações": 7,
    "Desarmes": 3,
    "Minutos jogados": 90
  }
}

Streamlit
Selecione o ID da partida e visualize o resumo:
Entrada: ID da partida: 3788741
Saída: "O time A venceu o time B por 3 a 1..."
Pesquise pelo nome de um jogador:
Entrada: Nome do jogador: Lionel Messi
Saída: Estatísticas exibidas em um JSON ou tabela.
