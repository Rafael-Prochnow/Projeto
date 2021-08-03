import pandas as pd
import numpy as np

df = pd.read_csv("Total_de_Tabela_2008.csv")

'''
df = pd.read_csv("Tabela_geral_2019_nova.csv")
df.drop('Unnamed: 0', axis=1, inplace=True)
df['Ar_Pts_C'] = df['Pts_3_C'] + df['Pts_2_C']
df['Ar_Pts_T'] = df['Pts_3_T'] + df['Pts_2_T']
df['posse_de_bola'] = df['Ar_Pts_T'] - df['RO'] + df['ER'] + (0.4 * df['LL_Pts_T'])
df['Min'] = df['Min'].str.replace(':', '.')
df['Min'] = df.Min.astype(float)'''

temporada = df[df['Jogador'] == 'Equipe']
# media_temporada = round(temporada.mean(), 1)
# desvio_padrao_temporada = round(temporada.std(), 0)
primeiro_quartil_temporada = temporada.quantile(q=0.25)
terceiro_quartil_temporada = temporada.quantile(q=0.75)

# media_times = round(temporada.groupby('Time').mean(), 1)
# desvio_padrao_times = round(temporada.groupby('Time').std(), 0)
# essa é a paprte do agrupamento para cada time
primeiro_quartil_times = temporada.groupby('Time').quantile(q=0.25)
terceiro_quartil_times = temporada.groupby('Time').quantile(q=0.75)

indicadores = ['Pts_C', 'Pts_T', 'Pts_3_C', 'Pts_3_T', 'Pts_2_C', 'Pts_2_T',
               'LL_C', 'LL_T', 'RO', 'RD', 'RT', 'AS', 'BR', 'TO', 'FC', 'FR',
               'ER', 'EN', 'Ar_Pts_C', 'Ar_Pts_T', 'posse_de_bola']

relatorio = pd.DataFrame()
relatorio['Times'] = primeiro_quartil_times.index

for x in indicadores:
    condition = [(primeiro_quartil_times[x] <= primeiro_quartil_temporada[x]) &
                 (terceiro_quartil_times[x] <= terceiro_quartil_temporada[x]),
                 (primeiro_quartil_times[x] >= primeiro_quartil_temporada[x]) &
                 (terceiro_quartil_times[x] <= terceiro_quartil_temporada[x]),
                 (primeiro_quartil_times[x] >= primeiro_quartil_temporada[x]) &
                 (terceiro_quartil_times[x] >= terceiro_quartil_temporada[x]),
                 (primeiro_quartil_times[x] <= primeiro_quartil_temporada[x]) &
                 (terceiro_quartil_times[x] >= terceiro_quartil_temporada[x])]

    choices = ['Baixo', 'Medio', 'Alto', 'N_padrao']
    relatorio[x] = np.select(condition, choices)

relatorio.to_csv("Avaliação.csv", index=None)
#################################################################################################################
# A análise do adversário é realizando substituindo o TIME por ADV

# essa é a parte do agrupamento para cada OPONENTE
primeiro_quartil_oponentes = temporada.groupby('Oponente').quantile(q=0.25)
terceiro_quartil_oponentes = temporada.groupby('Oponente').quantile(q=0.75)

relatorio_oponentes = pd.DataFrame()
relatorio_oponentes['Oponente'] = primeiro_quartil_oponentes.index

for x in indicadores:
    condition = [(primeiro_quartil_oponentes[x] <= primeiro_quartil_temporada[x]) &
                 (terceiro_quartil_oponentes[x] <= terceiro_quartil_temporada[x]),
                 (primeiro_quartil_oponentes[x] >= primeiro_quartil_temporada[x]) &
                 (terceiro_quartil_oponentes[x] <= terceiro_quartil_temporada[x]),
                 (primeiro_quartil_oponentes[x] >= primeiro_quartil_temporada[x]) &
                 (terceiro_quartil_oponentes[x] >= terceiro_quartil_temporada[x]),
                 (primeiro_quartil_oponentes[x] <= primeiro_quartil_temporada[x]) &
                 (terceiro_quartil_oponentes[x] >= terceiro_quartil_temporada[x])]

    choices = ['Baixo', 'Medio', 'Alto', 'N_padrao']
    relatorio_oponentes[x] = np.select(condition, choices)

relatorio_oponentes.to_csv("Avaliação_oponente.csv", index=None)
#######################################################################################################################
# A ANÁLISE AVANÇADA

analise = pd.DataFrame()
analise['Temporada'] = df['Temporada']  # temporada
analise['Time'] = df['Time']  # time
analise['Oponente'] = df['Oponente']  # adversário
analise['Casa/Fora'] = df['Casa/Fora']  # casa/fora
analise['Jogador'] = df['Jogador']  # Jogadores
analise['Min'] = df['Min']  # minutos
analise['EF_Pts'] = round(df['Pts_C'] / df['Pts_T'], 3)  # eficiência dos pontos totais
analise['FR_3_Pts_C'] = round((df['Pts_3_C'] * 3) / df['Pts_C'], 3)  # frequência relativa do 3 pontos convertidos
analise['FR_3_Pts_T'] = round((df['Pts_3_T'] * 3) / df['Pts_T'], 3)  # frequência relativa do 3 pontos tentados
analise['EF_Pts_3'] = round(df['Pts_3_C'] / df['Pts_3_T'], 3)  # eficiência dos 3 pontos
analise['FR_2_Pts_C'] = round((df['Pts_2_C'] * 2) / df['Pts_C'], 3)  # frequência relativa do 2 pontos convertidos
analise['FR_2_Pts_T'] = round((df['Pts_2_T'] * 2) / df['Pts_T'], 3)  # frequência relativa do 2 pontos tentados
analise['EF_Pts_2'] = round(df['Pts_2_C'] / df['Pts_2_T'], 3)  # eficiência dos 2 pontos
analise['FR_LL_C'] = round(df['LL_C'] / df['Pts_C'], 3)  # frequência relativa dos Lances Livres convertidos
analise['FR_LL_T'] = round(df['LL_T'] / df['Pts_T'], 3)  # frequência relativa dos Lances Livres tentados
analise['EF_LL'] = round(df['LL_C'] / df['LL_T'], 3)  # eficiência dos Lances Livres
# analise['Pace']
# four fectores
analise['eFG_%'] = round((df['Ar_Pts_C'] + 0.5 * df['Pts_3_C']) / df['Ar_Pts_T'], 3)  # aproveitamento efetivo
analise['TOV_%'] = round(100 * df['ER'] / (df['Ar_Pts_T'] + 0.475 * df['LL_T'] + df['ER']), 1)  # fator turnover
analise['FTA/FGA'] = round(df['LL_T'] / df['Ar_Pts_C'], 3)  # fator de aproveitamento dos lances livres
# analise['ORB%'] =  # precisa do resultado do time adv
analise['Posse_de_Bola'] = df['posse_de_bola']   # posse de bola
analise['Offensive_Rating'] = 100 * round(df['Pts_C']/df['posse_de_bola'], 3)  # pontos por posse de bola/por 100 posses
analise['TS_%'] = round(df['Pts_C'] / (2*(df['Ar_Pts_T'] + 0.475 * df['LL_T'])), 3)  # porcentagem dos arremessos
analise['Ass/ER'] = round(df['AS'] / df['ER'], 3)  # assistência por erros
analise['AS_Ratio'] = 100 * round((df['AS'] / df['posse_de_bola']), 3)  # assistências por posse de bola
analise.reset_index()
# depois de aplicar para todos os indicadores selecionamos apenas os times

temporada_avc = analise[analise['Jogador'] == 'Equipe']
primeiro_quartil_temporada_avc = temporada_avc.quantile(q=0.25)
terceiro_quartil_temporada_avc = temporada_avc.quantile(q=0.75)
# essa é a paprte do agrupamento para cada time
primeiro_quartil_times_avc = temporada_avc.groupby('Time').quantile(q=0.25)
terceiro_quartil_times_avc = temporada_avc.groupby('Time').quantile(q=0.75)

indicadores_avc = ['EF_Pts', 'FR_3_Pts_C', 'FR_3_Pts_T', 'EF_Pts_3', 'FR_2_Pts_C', 'FR_2_Pts_T',
                   'EF_Pts_2', 'FR_LL_C', 'FR_LL_T', 'EF_LL', 'eFG_%', 'TOV_%', 'FTA/FGA',
                   'Posse_de_Bola', 'Offensive_Rating', 'TS_%', 'Ass/ER', 'AS_Ratio']

relatorio_avc = pd.DataFrame()
relatorio_avc['Times'] = primeiro_quartil_times_avc.index

for x in indicadores_avc:
    condition = [(primeiro_quartil_times_avc[x] <= primeiro_quartil_temporada_avc[x]) &
                 (terceiro_quartil_times_avc[x] <= terceiro_quartil_temporada_avc[x]),
                 (primeiro_quartil_times_avc[x] >= primeiro_quartil_temporada_avc[x]) &
                 (terceiro_quartil_times_avc[x] <= terceiro_quartil_temporada_avc[x]),
                 (primeiro_quartil_times_avc[x] >= primeiro_quartil_temporada_avc[x]) &
                 (terceiro_quartil_times_avc[x] >= terceiro_quartil_temporada_avc[x]),
                 (primeiro_quartil_times_avc[x] <= primeiro_quartil_temporada_avc[x]) &
                 (terceiro_quartil_times_avc[x] >= terceiro_quartil_temporada_avc[x])]

    choices = ['Baixo', 'Medio', 'Alto', 'N_padrao']
    relatorio_avc[x] = np.select(condition, choices)

relatorio_avc.to_csv("Avaliação_avançada.csv", index=None)
########################################################################################################################
# ANÁLISE AVANÇADA DO OPONENTE
# apenas trocar o TIME por Adv
primeiro_quartil_oponentes_avc = temporada_avc.groupby('Oponente').quantile(q=0.25)
terceiro_quartil_oponentes_avc = temporada_avc.groupby('Oponente').quantile(q=0.75)


relatorio_oponentes_avc = pd.DataFrame()
relatorio_oponentes_avc['Oponente'] = primeiro_quartil_oponentes_avc.index

for x in indicadores_avc:
    condition = [(primeiro_quartil_oponentes_avc[x] <= primeiro_quartil_temporada_avc[x]) &
                 (terceiro_quartil_oponentes_avc[x] <= terceiro_quartil_temporada_avc[x]),
                 (primeiro_quartil_oponentes_avc[x] >= primeiro_quartil_temporada_avc[x]) &
                 (terceiro_quartil_oponentes_avc[x] <= terceiro_quartil_temporada_avc[x]),
                 (primeiro_quartil_oponentes_avc[x] >= primeiro_quartil_temporada_avc[x]) &
                 (terceiro_quartil_oponentes_avc[x] >= terceiro_quartil_temporada_avc[x]),
                 (primeiro_quartil_oponentes_avc[x] <= primeiro_quartil_temporada_avc[x]) &
                 (terceiro_quartil_oponentes_avc[x] >= terceiro_quartil_temporada_avc[x])]

    choices = ['Baixo', 'Medio', 'Alto', 'N_padrao']
    relatorio_oponentes_avc[x] = np.select(condition, choices)

relatorio_oponentes_avc.to_csv("Avaliação_oponente_avançada.csv", index=None)



# OPONENTE

df = pd.read_csv("Tabela_geral_2019_nova.csv")
df.drop('Unnamed: 0', axis=1, inplace=True)
df['Ar_Pts_C'] = df['Pts_3_C'] + df['Pts_2_C']
df['Ar_Pts_T'] = df['Pts_3_T'] + df['Pts_2_T']
df['posse_de_bola'] = df['Ar_Pts_T'] - df['RO'] + df['ER'] + (0.4 * df['LL_Pts_T'])
df['Min'] = df['Min'].str.replace(':', '.')
df['Min'] = df.Min.astype(float)

temporada = df[df['Jogador'] == 'Equipe']

# print(relatorio_oponentes)
########################################################################################################################

analise = pd.DataFrame()
analise['Temporada'] = df['Temporada']  # temporada
analise['Time'] = df['Time']  # time
analise['Adv'] = df['Adv']  # adversário
analise['C_F'] = df['C_F']  # casa/fora
analise['Jogador'] = df['Jogador']  # Jogadores
analise['Min'] = df['Min']  # minutos
analise['EF_Pts'] = round(df['Pts_C'] / df['Pts_T'], 3) # eficiência dos pontos totais
analise['FR_3_Pts_C'] = round((df['Pts_3_C'] * 3) / df['Pts_C'], 3)  # frequência relativa do 3 pontos convertidos
analise['FR_3_Pts_T'] = round((df['Pts_3_T'] * 3) / df['Pts_T'], 3)  # frequência relativa do 3 pontos tentados
analise['EF_Pts_3'] = round(df['Pts_3_C'] / df['Pts_3_T'], 3)  # eficiência dos 3 pontos
analise['FR_2_Pts_C'] = round((df['Pts_2_C'] * 2) / df['Pts_C'], 3)  # frequência relativa do 2 pontos convertidos
analise['FR_2_Pts_T'] = round((df['Pts_2_T'] * 2) / df['Pts_T'], 3)  # frequência relativa do 2 pontos tentados
analise['EF_Pts_2'] = round(df['Pts_2_C'] / df['Pts_2_T'], 3)  # eficiência dos 2 pontos
analise['FR_LL_C'] = round(df['LL_Pts_C'] / df['Pts_C'], 3)  # frequência relativa dos Lances Livres convertidos
analise['FR_LL_T'] = round(df['LL_Pts_T'] / df['Pts_T'], 3)  # frequência relativa dos Lances Livres tentados
analise['EF_LL'] = round(df['LL_Pts_C'] / df['LL_Pts_T'], 3)  # eficiência dos Lances Livres
# analise['Pace']
# four fectores
analise['eFG_%'] = round((df['Ar_Pts_C'] + 0.5 * df['Pts_3_C']) / df['Ar_Pts_T'], 3)  #  aproveitamento efetivo
analise['TOV_%'] = round(100 * df['ER'] / (df['Ar_Pts_T'] + 0.475 * df['LL_Pts_T'] + df['ER']), 1)  # fator turnover
analise['FTA/FGA'] = round(df['LL_Pts_T'] / df['Ar_Pts_C'], 3)  # fator de aproveitamento dos lances livres
# analise['ORB%'] =  # precisa do resultado do time adv
analise['Posse_de_Bola'] = df['posse_de_bola']   # posse de bola
analise['Offensive_Rating'] = 100 * round(df['Pts_C']/df['posse_de_bola'], 3) # pontos por posse de bola com o ajusto de 100 posses
analise['TS_%'] = round(df['Pts_C'] / (2*(df['Ar_Pts_T'] + 0.475 * df['LL_Pts_T'])), 3)  # porcentagem dos arremessos
analise['Ass/ER'] = round(df['AS'] / df['ER'], 3)  # assistência por erros
analise['AS_Ratio'] = 100 * round((df['AS'] / df['posse_de_bola']), 3)  # assistências por posse de bola
analise.reset_index()