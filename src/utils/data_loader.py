import pandas as pd

def carregar_dados():
    df_matches = pd.read_csv('data/processed/df_dados_matches.csv')
    df_players = pd.read_csv('data/processed/df_dados_players.csv', index_col=0)
    df_teams = pd.read_csv('data/processed/df_dados_teams.csv', index_col=0)
    return df_matches, df_players, df_teams

def preparar_dados_times(df_matches):
    df_matches['TotalGols'] = df_matches['FullTimeHomeGoals'] + df_matches['FullTimeAwayGoals']
    df_matches['PtsHome'] = df_matches['FullTimeResult'].map({'H': 3, 'D': 1, 'A': 0})
    df_matches['PtsAway'] = df_matches['FullTimeResult'].map({'H': 0, 'D': 1, 'A': 3})
    return df_matches

def preparar_pontos(df_matches):
    pts_casa = df_matches.groupby(['HomeTeam', 'Season'])['PtsHome'].sum().reset_index()
    pts_casa.columns = ['Team', 'Season', 'Pts']
    pts_fora = df_matches.groupby(['AwayTeam', 'Season'])['PtsAway'].sum().reset_index()
    pts_fora.columns = ['Team', 'Season', 'Pts']
    df_pontos = pd.concat([pts_casa, pts_fora], ignore_index=True)
    pts_total = df_pontos.groupby(['Team', 'Season'])['Pts'].sum().reset_index()
    return pts_total