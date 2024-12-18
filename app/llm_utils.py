import openai
import os
from dotenv import load_dotenv
from data_utils import get_match_data

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_match(match_id: int):
    """
    Usa LLM para gerar a sumarização textual da partida utilizando a nova API de chat completions.
    """
    # Extrai os eventos da partida
    events = get_match_data(match_id)

    print("=== Dados Carregados ===")
    print(events.head())

    # Verifica se há eventos
    if events.empty:
        return "Não foram encontrados eventos para a partida fornecida."

    # Verifica os tipos de eventos disponíveis
    print("=== Tipos de Eventos Disponíveis ===")
    print(events['type'].unique())

    # Filtra os principais eventos relevantes
    highlights = events[events['type'].isin(['Shot', 'Own Goal Against', 'Own Goal For', 'Foul Committed', 'Foul Won'])]

    print("=== Eventos Filtrados ===")
    print(highlights[['type', 'team', 'player', 'minute']].head())

    # Verifica se há eventos relevantes
    if highlights.empty:
        return "Nenhum evento principal encontrado na partida."

    # Prepara o prompt para o LLM
    prompt = (
        "Com base nos eventos destacados da partida, elabore uma sumarização detalhada "
        "incluindo gols, chutes, faltas e principais momentos:\n"
        f"{highlights[['type', 'team', 'player', 'minute']].to_string(index=False)}"
    )

    # Chama o modelo da OpenAI para gerar o texto
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use "gpt-4" se disponível
        messages=[
            {"role": "system", "content": "Você é um assistente que gera sumarizações de partidas de futebol."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400
    )

    # Retorna o conteúdo gerado
    return response["choices"][0]["message"]["content"]

# Teste simples
if __name__ == "__main__":
    test_match_id = 3788741  # Substitua por um ID de partida válido
    print("=== Sumarização da Partida ===")
    try:
        summary = summarize_match(test_match_id)
        print(summary)
    except Exception as e:
        print(f"Erro ao executar a sumarização: {e}")

def generate_narration(events, style="formal"):
    """
    Gera uma narração personalizada com base nos eventos da partida e no estilo escolhido.
    
    Args:
        events (DataFrame): DataFrame com eventos da partida.
        style (str): Estilo de narração ('formal', 'humoristico', 'tecnico').
    
    Returns:
        str: Texto com a narração personalizada.
    """
    # Garantir que os eventos relevantes estão presentes
    if events.empty:
        return "Nenhum evento relevante encontrado na partida."

    # Prepara os eventos para inclusão na narração
    highlights = events[['minute', 'type', 'team', 'player']].to_dict('records')

    # Estilos de narração
    if style == "formal":
        narration = "Resumo Formal da Partida:\n"
        for event in highlights:
            narration += (
                f"No minuto {event['minute']}, "
                f"{event['player']} do time {event['team']} realizou uma ação do tipo {event['type']}.\n"
            )

    elif style == "humoristico":
        narration = "Resumo Humorístico da Partida:\n"
        for event in highlights:
            narration += (
                f"No minuto {event['minute']}, {event['player']} do {event['team']} fez um {event['type']} "
                f"que deixou todo mundo surpreso! Que momento épico!\n"
            )
    
    elif style == "tecnico":
        narration = "Análise Técnica da Partida:\n"
        for event in highlights:
            narration += (
                f"Aos {event['minute']} minutos, o jogador {event['player']} do {event['team']} executou "
                f"um evento do tipo {event['type']}, contribuindo para a dinâmica tática da equipe.\n"
            )
    
    else:
        return "Estilo de narração inválido. Escolha entre 'formal', 'humoristico' ou 'tecnico'."

    return narration

if __name__ == "__main__":
    test_match_id = 3788741  # Substitua por um ID válido

    # Obtenha os eventos filtrados
    events = get_match_data(test_match_id)
    relevant_events = events[events['type'].isin(['Shot', 'Goal', 'Foul Committed', 'Substitution'])]

    # Teste os diferentes estilos
    print("=== Narração Formal ===")
    print(generate_narration(relevant_events, style="formal"))

    print("\n=== Narração Humorística ===")
    print(generate_narration(relevant_events, style="humoristico"))

    print("\n=== Narração Técnica ===")
    print(generate_narration(relevant_events, style="tecnico"))


