from statsbombpy import sb
import pandas as pd

def get_match_data(match_id: int):
    """
    Extrai os dados brutos de uma partida específica.
    """
    events = sb.events(match_id=match_id)
    return events

def get_player_stats(match_id: int, player_name: str):
    """
    Retorna estatísticas de um jogador específico na partida.
    """
    events = get_match_data(match_id)
    player_events = events[events['player'] == player_name]
    stats = {
        "Passes": len(player_events[player_events['type'] == 'Pass']),
        "Finalizações": len(player_events[player_events['type'] == 'Shot']),
        "Desarmes": len(player_events[player_events['type'] == 'Duel']),
        "Minutos jogados": player_events['minute'].max()
    }
    return stats

if __name__ == "__main__":
   
    test_match_id = 3788741  
    test_player_name = "Manuel Locatelli" 

    print("=== Testando get_player_stats ===")
    try:
        player_stats = get_player_stats(test_match_id, test_player_name)
        print(f"Estatísticas de {test_player_name}:")
        print(player_stats)
    except Exception as e:
        print(f"Erro ao executar o teste: {e}")