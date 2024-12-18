from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from app.data_utils import get_player_stats
from statsbombpy import sb


def get_event_summary(match_id, event_type):
    """
    Retorna eventos específicos da partida, filtrados pelo tipo (e.g., 'Pass', 'Shot').
    """
    events = sb.events(match_id=match_id)
    filtered_events = events[events['type'] == event_type]
    summary = filtered_events[['minute', 'team', 'player']].to_dict(orient="records")
    return summary

def get_match_summary(match_id):
    """
    Retorna um resumo geral da partida, incluindo o placar final, autores dos gols e principais eventos.
    """
    events = sb.events(match_id=match_id)
    # Filtra os eventos relevantes
    goals = events[(events['type'] == 'Shot') & (events['outcome'] == 'Goal')]
    summary = {
        "Placar Final": f"{events['home_score'].iloc[0]} - {events['away_score'].iloc[0]}",
        "Gols": goals[['minute', 'team', 'player']].to_dict(orient="records"),
    }
    return summary

def compare_players(match_id, player1, player2, metric):
    """
    Compara dois jogadores em uma métrica específica (e.g., 'Passes', 'Shots').
    """
    stats_player1 = get_player_stats(match_id, player1)
    stats_player2 = get_player_stats(match_id, player2)

    comparison = {
        player1: stats_player1.get(metric, 0),
        player2: stats_player2.get(metric, 0)
    }

    # Determinar o vencedor
    if comparison[player1] > comparison[player2]:
        winner = player1
    elif comparison[player2] > comparison[player1]:
        winner = player2
    else:
        winner = "Empate"

    comparison['Vencedor'] = winner
    return comparison

def create_agent():
    tools = [
        Tool(
            name="Player Stats",
            func=lambda x: get_player_stats(x['match_id'], x['player_name']),
            description="Consulta estatísticas de um jogador específico, como passes, finalizações e desarmes."
        ),
        Tool(
            name="Match Summary",
            func=lambda x: get_event_summary(x['match_id'], x['event_type']),
            description="Consulta eventos específicos da partida, como passes ou chutes ao gol."
        ),
        Tool(
            name="Compare Players",
            func=lambda x: compare_players(x['match_id'], x['player1'], x['player2'], x['metric']),
            description="Compara dois jogadores em uma métrica específica, como passes ou finalizações."
        )
    ]

    llm = OpenAI(temperature=0)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    return agent
