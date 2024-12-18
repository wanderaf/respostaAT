import openai
import pandas as pd
import os
from dotenv import load_dotenv
from data_utils import get_match_data

def summarize_match(match_id: int):
    """
    Usa LLM para gerar a sumarização textual da partida utilizando a nova API de chat completions.
    """
    # Extrai os eventos da partida
    events = get_match_data(match_id)

    # Depuração: Verifique se os dados foram carregados corretamente
    print("=== Dados Carregados ===")
    if events is None:
        print("Erro: Nenhum dado foi retornado.")
        return "Erro: Nenhum dado foi retornado."

    if not isinstance(events, pd.DataFrame):
        print("Erro: Os dados retornados não são um DataFrame.")
        return "Os dados não estão no formato esperado."

    print(events.head())  # Exibe as primeiras linhas do DataFrame

    # Verifica se há eventos
    if events.empty:
        return "Não foram encontrados eventos para a partida fornecida."

    # Verifica os tipos de eventos disponíveis
    print("=== Tipos de Eventos Disponíveis ===")
    if 'type' in events.columns:
        print(events['type'].unique())
    else:
        print("A coluna 'type' não está presente nos dados.")
        return "A coluna 'type' não está presente nos dados."

    # Filtra os principais eventos (gols, cartões, etc.)
    highlights = events[events['type'].isin(['Goal', 'Card'])]

    # Verifica se há eventos relevantes
    if highlights.empty:
        return "Nenhum evento principal encontrado na partida."

    # Prepara o prompt para o LLM
    prompt = f"Resuma os principais eventos desta partida:\n{highlights}"

    # Chama o modelo da OpenAI para gerar o texto
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use "gpt-4" se disponível
        messages=[
            {"role": "system", "content": "Você é um assistente que resume partidas de futebol."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
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
