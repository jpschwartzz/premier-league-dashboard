from src.utils.data_loader import carregar_dados, preparar_dados_times, preparar_pontos
from src.components.charts import (grafico_media_gols, grafico_campeoes,
                                    grafico_rebaixados, grafico_torcida,
                                    grafico_artilheiros, grafico_decisivos)
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import numpy as np

# Carregando dados
df_matches, df_players, df_teams = carregar_dados()

# Preparando dados
df_matches = preparar_dados_times(df_matches)
pts_total = preparar_pontos(df_matches)

# Campeões
df_campeoes = pts_total.loc[pts_total.groupby('Season')['Pts'].idxmax()]
titulos = df_campeoes['Team'].value_counts().reset_index()
titulos.columns = ['Team', 'Titulos']

# Rebaixados
df_rebaixados = pts_total.sort_values('Pts').groupby('Season').head(3)
n_rebaixados = df_rebaixados.value_counts('Team').reset_index()

# Torcida
import numpy as np
condicoes_torcida = [
    (df_matches['Season'] == '2019/20') | (df_matches['Season'] == '2020/21'),
    df_matches['Season'] > '2020/21',
    df_matches['Season'] < '2019/20'
]
valores_torcida = ['Pandemia (Sem torcida)', 'Depois da pandemia', 'Antes da pandemia']
df_matches['Periodo'] = np.select(condicoes_torcida, valores_torcida, default='')
df_torcida = df_matches.groupby('Periodo')['FullTimeResult'].apply(lambda x: (x == 'H').mean() * 100).reset_index(name='Pct_Vitorias_Casa')

# Jogadores
media_gols = df_matches.groupby('Season')['TotalGols'].mean().reset_index()
df_artilheiros = df_players.sort_values(by='Gls', ascending=False).head(10)
df_decisivos = df_players.sort_values(by='G+A', ascending=False).head(10)
df_decisivos = df_decisivos.rename(columns={'Gls': 'Gols', 'Ast': 'Assistências'})

fig_media_gols = grafico_media_gols(media_gols)
fig_campeoes = grafico_campeoes(titulos)
fig_rebaixados = grafico_rebaixados(n_rebaixados)
fig_torcida = grafico_torcida(df_torcida)
fig_artilheiros = grafico_artilheiros(df_artilheiros)
fig_decisivos = grafico_decisivos(df_decisivos)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div([
    html.H1('⚽ Premier League Dashboard',
            style={'textAlign': 'center', 'padding': '20px'}),
    dbc.Tabs([
        dbc.Tab(label='Times', tab_id='tab-times'),
        dbc.Tab(label='Jogadores', tab_id='tab-jogadores'),
    ], id='tabs', active_tab='tab-times'),
    html.Div(id='conteudo-abas')
])

@app.callback(
    Output('conteudo-abas', 'children'),
    Input('tabs', 'active_tab')
)
def renderizar_aba(aba):
    if aba == 'tab-times':
        return html.Div([
            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig_media_gols), width=6),
                dbc.Col(dcc.Graph(figure=fig_campeoes), width=6),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig_rebaixados), width=6),
                dbc.Col(dcc.Graph(figure=fig_torcida), width=6),
            ]),
    ])
    elif aba == 'tab-jogadores':
        return html.Div([
            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig_artilheiros), width=6),
                dbc.Col(dcc.Graph(figure=fig_decisivos), width=6),
            ]),
        ])

if __name__ == '__main__':
    app.run(debug=True)