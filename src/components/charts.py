import plotly.express as px

def grafico_media_gols(media_gols):
    fig = px.line(media_gols, x='Season', y='TotalGols',
                  labels={'TotalGols': 'Média de Gols', 'Season': 'Temporada'},
                  title='Média de Gols por Temporada')
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def grafico_campeoes(titulos):
    fig = px.bar(titulos, x='Team', y='Titulos',
                 labels={'Team': 'Clube', 'Titulos': 'Títulos'},
                 title='Campeões da Premier League 2000-2025')
    fig.update_layout(title_x=0.5)
    return fig

def grafico_rebaixados(n_rebaixados):
    fig = px.bar(n_rebaixados.head(10), x='Team', y='count',
                 labels={'count': 'Número de vezes', 'Team': 'Clube'},
                 title='Top 10 mais rebaixados da Premier League 2000-2025')
    fig.update_layout(title_x=0.5, xaxis_tickangle=-45)
    return fig

def grafico_torcida(df_torcida):
    fig = px.bar(df_torcida, x='Periodo', y='Pct_Vitorias_Casa',
                 labels={'Periodo': 'Período', 'Pct_Vitorias_Casa': 'Porcentagem de vitórias em casa'},
                 category_orders={"Periodo": ['Antes da pandemia', 'Pandemia (Sem torcida)', 'Depois da pandemia']},
                 title='Comparação de vitória com e sem torcida jogando em casa')
    fig.update_layout(title_x=0.5)
    return fig

def grafico_artilheiros(df_artilheiros):
    fig = px.bar(df_artilheiros, x='Player', y='Gls',
                 labels={'Player': 'Jogador', 'Gls': 'Gols'},
                 title='Top 10 Artilheiros 2024/25')
    fig.update_layout(xaxis_tickangle=-45, title_x=0.5)
    return fig

def grafico_decisivos(df_decisivos):
    fig = px.bar(df_decisivos, x='Player', y=['Gols', 'Assistências'],
                 barmode='stack',
                 labels={'Player': 'Jogador', 'value': 'Gols + Assistências'},
                 title='Top 10 Mais Decisivos 2024/25')
    fig.update_layout(xaxis_tickangle=-45, legend_title_text='', title_x=0.5)
    return fig