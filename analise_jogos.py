import pandas as pd
import os

# Forçando o script a usar onde a pasta está, pois não estava lendo o arquivo games.csv
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Carregando os datasets
games = pd.read_csv('games.csv')
player_stats = pd.read_csv('player_stats.csv')

# Juntando os dados usando AppID/GameID
df = pd.merge(games, player_stats, left_on='AppID', right_on='GameID', how='inner')

# Separando por tarefa
print('\nTarefa 1' + 10*'___')

# Separando os gêneros em linhas
df_exploded = df.copy()
df_exploded['Genre'] = df_exploded['Genre'].str.split(';')
df_exploded = df_exploded.explode('Genre')

# Limpando espaços nos gêneros
df_exploded['Genre'] = df_exploded['Genre'].str.strip()

# Calculando a média de horas por gênero
genre_avg_playtime = df_exploded.groupby('Genre')['Average_Playtime_Hours'].mean().sort_values(ascending=False)

# Transformando em DataFrame, para os dados ficarem mais bonitos na visualização
genre_avg_playtime_df = genre_avg_playtime.reset_index()

# Formatando para 2 casas decimais após a vírgula
genre_avg_playtime_df['Average_Playtime_Hours'] = genre_avg_playtime_df['Average_Playtime_Hours'].map(lambda x: f'{x:.2f}')

# E por fim, mostrando o resultado
print('Média de horas jogadas por gênero:')
print(genre_avg_playtime_df.to_string(index=False))
# Esse último print, serve para imprimir o DataFrame de forma limpa, sem mostrar o índice e com alinhamento mais charmoso

# Conclusão da primeira tarefa:
# O gênero com maior média de horas jogadas foi MOBA, com uma média de 550 horas.

# Separando por tarefa
print('\nTarefa 2' + 10*'___')

# Filtrando os jogos com mais de 95% de avaliações positivas e menos de 50 horas
hidden_gems = df[(df['Positive_Ratings_Percent'] > 95) & (df['Average_Playtime_Hours'] < 50)]

# Mostrando o resultado
print('Jogos com mais de 95% de avaliações positivas e menos de 50h de jogo:')
print(hidden_gems[['Name', 'Average_Playtime_Hours', 'Positive_Ratings_Percent']])

# Conclusão da segunda tarefa:
# Estes jogos são as tals gemas escondidas, pois são muito bem avaliados e curtos, bons para jogar nos dias de semana.

# Separando por tarefa
print('\nTarefa 3' + 10*'___')

# Criando a coluna de Índice de Retenção (tratando os jogos gratuitos)
df['Indice_Retencao'] = df.apply(lambda row: row['Average_Playtime_Hours'] / row['Price'] if row['Price'] > 0 else None, axis=1)

# Mostrando o resultado
print('DataFrame com coluna Indice_Retencao:')
print(df[['Name', 'Price', 'Average_Playtime_Hours', 'Indice_Retencao']])

# Conclusão do código:
# Para jogos gratuitos, o índice foi definido como None(NaN) para evitar a divisão por zero, com isso, o jogo com maior indice é o Terraria e o menor é o HELLDIVERS 2.
