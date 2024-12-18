import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsbombpy import sb
from app.data_utils import get_player_stats
from app.llm_utils import summarize_match

# Configuração inicial
st.sidebar.title("Navegação")
page = st.sidebar.selectbox(
    "Escolha a funcionalidade",
    [
        "Sumarização da Partida",
        "Estatísticas de um Jogador",
        "Filtros de Eventos",
        "Comparação de Jogadores"
    ]
)

# Função para carregar dados gerais
@st.cache_data
def load_data(match_id):
    try:
        events = sb.events(match_id=match_id)
        player_names = events['player'].dropna().unique()
        return events, player_names
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return None, None

# Obter competições e temporadas
competitions = sb.competitions()
competition_id = st.sidebar.selectbox("Selecione a Competição", competitions['competition_id'].unique())
season_id = st.sidebar.selectbox("Selecione a Temporada", competitions[competitions['competition_id'] == competition_id]['season_id'].unique())
matches = sb.matches(competition_id=competition_id, season_id=season_id)
match_options = matches[['match_id', 'home_team', 'away_team']].apply(
    lambda row: f"{row['match_id']} - {row['home_team']} vs {row['away_team']}", axis=1
)
match_id = st.sidebar.selectbox("Selecione a Partida", match_options)
match_id = int(match_id.split(" - ")[0])  # Extrair o ID da partida

# Carregar dados da partida
events, player_names = load_data(match_id)

# Página: Sumarização da Partida
if page == "Sumarização da Partida":
    st.title("Sumarização da Partida")
    if st.button("Gerar Sumarização"):
        try:
            summary = summarize_match(match_id)
            st.write(summary)
        except Exception as e:
            st.error(f"Erro ao gerar a sumarização: {e}")

# Página: Estatísticas de um Jogador
elif page == "Estatísticas de um Jogador":
    st.title("Estatísticas de um Jogador")
    if player_names is not None:
        selected_player = st.selectbox("Selecione o Jogador", player_names)
        if st.button("Exibir Estatísticas"):
            try:
                stats = get_player_stats(match_id, selected_player)
                stats_df = pd.DataFrame(stats.items(), columns=["Estatística", "Valor"])
                st.dataframe(stats_df)

                # Gráfico de barras das estatísticas
                st.subheader("Gráfico de Estatísticas")
                stats_df.set_index("Estatística").plot(kind="bar", legend=False, figsize=(8, 5))
                plt.title(f"Estatísticas de {selected_player}")
                plt.ylabel("Quantidade")
                st.pyplot(plt)
            except Exception as e:
                st.error(f"Erro ao exibir as estatísticas: {e}")

# Página: Filtros de Eventos
elif page == "Filtros de Eventos":
    st.title("Exploração de Eventos Específicos")
    if events is not None:
        event_types = events['type'].unique()

        # Garantir que os valores padrão estão disponíveis
        default_event_types = ["Goal", "Card"]
        available_defaults = [event for event in default_event_types if event in event_types]

        # Filtro para explorar eventos específicos
        event_filter = st.multiselect(
            "Filtrar Eventos Específicos",
            event_types,
            default=available_defaults  # Usar apenas valores que existem nas opções
        )

        filtered_events = events[events['type'].isin(event_filter)]

        st.subheader("Eventos Filtrados")
        st.dataframe(filtered_events[['minute', 'team', 'player', 'type']])

# Página: Comparação de Jogadores
elif page == "Comparação de Jogadores":
    st.title("Comparação de Jogadores")
    if player_names is not None:
        player_name1 = st.selectbox("Selecione o Primeiro Jogador", player_names)
        player_name2 = st.selectbox("Selecione o Segundo Jogador", player_names)

        if st.button("Comparar Jogadores"):
            try:
                stats_player1 = get_player_stats(match_id, player_name1)
                stats_player2 = get_player_stats(match_id, player_name2)

                # Mostrar tabelas comparativas
                st.subheader("Comparação Entre Jogadores")
                comparison_data = pd.DataFrame([stats_player1, stats_player2], index=[player_name1, player_name2])
                st.dataframe(comparison_data)

                # Gráfico de barras comparativo
                st.subheader("Gráfico Comparativo")
                comparison_data.T.plot(kind="bar", figsize=(10, 6))
                plt.title("Comparação Estatística")
                plt.ylabel("Quantidade")
                st.pyplot(plt)
            except Exception as e:
                st.error(f"Erro ao realizar a comparação: {e}")
