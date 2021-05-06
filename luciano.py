import pandas as pd
import os
from datetime import datetime
import re
import matplotlib.pyplot as plt
import seaborn as sns
from funcoes import siglas, limpeza_tempo, transformar_segundos, quartos_do_jogo, resultado_da_posse_de_bola,\
    juntar_posses

path = r'C:/Users/Elen- PC/PycharmProjects/untitled1/Dados01/temporada 2018'
files = os.listdir(path)


files_csv = [path + '\\' + f for f in files if f[-3:] == 'csv']
df_posse = pd.DataFrame()
'''
data = pd.read_csv(files_csv[14])
arquivo_time = files_csv[15].replace('C:/Users/Elen- PC/PycharmProjects/untitled1/Dados01/temporada 2020', '')
arquivo_time = arquivo_time.replace('. C.', '')
print(arquivo_time)
expressao_regular = re.findall(r'[A-Z].*?[.]', arquivo_time)[0]
print(expressao_regular)
expressao_regular = expressao_regular.replace('.', '')
expressao_regular1 = expressao_regular.split('_x_')
casa = expressao_regular1[0]
nome_time_casa = casa.replace("'", "")
fora = expressao_regular1[1]
nome_time_fora = fora.replace(".'", "")

'''
aaa = 1
for f in files_csv:
    print(aaa)
    print(f)
    aaa += 1
    df = pd.read_csv(f)
    arquivo_time = f.replace('C:/Users/Elen- PC/PycharmProjects/untitled1/Dados01/temporada 2018', '')
    arquivo_time = arquivo_time.replace('. C.', '')
    expressao_regular = re.findall(r'[A-Z].*?[.]', arquivo_time)[0]
    expressao_regular = expressao_regular.replace('.', '')
    expressao_regular1 = expressao_regular.split('_x_')
    casa1 = expressao_regular1[0]
    nome_time_casa = casa1.replace("'", "")
    print(nome_time_casa)
    fora1 = expressao_regular1[1]
    nome_time_fora = fora1.replace(".'", "")
    print(nome_time_fora)
    data_hoje = datetime.today().strftime('%d/%m/%Y')
    dia_do_jogo = '02/01/2021'
    temporada = 2019
    sigla_time_a = siglas(nome_time_casa)
    sigla_time_b = siglas(nome_time_fora)
    casa = 'casa'
    fora = 'fora'
    classificatoria = '1 Turno'

    # Limpeza dos dados
    df = limpeza_tempo(df)

    # modificar o tempo decrescente para crescente (* -1)
    # acrescentar o tempo de cada quarto (primeiro quarto termina em 600s, o segundo quarto 2*600 = 1200 ...)
    df = transformar_segundos(df)

    # Acrescentado colunas
    # diferenca_placar_casa
    # diferenca_placar_visitante
    df['diferenca_placar_casa'] = df['placar_casa'] - df['placar_visitante']
    df['diferenca_placar_visitante'] = df['placar_visitante'] - df['placar_casa']
    df["diferenca_placar_absoluto"] = df.loc[:, "diferenca_placar_casa"].abs()

    # Analise da pontuação dos times
    pontuacao = df[(df['Indicador'] == '3_Pts_C') | (df['Indicador'] == '3_Pts_T') |
                   (df['Indicador'] == '2_Pts_C') | (df['Indicador'] == '2_Pts_T') |
                   (df['Indicador'] == 'LL_Pts_C') | (df['Indicador'] == 'LL_Pts_T') |
                   (df['Indicador'] == 'EN') |
                   (df['Indicador'] == 'fim_partida')]

    # estamos invertendo os valores para deixar parecido com o jogo
    pontuacao = pontuacao[::-1]
    pontuacao.reset_index(drop=True, inplace=True)

    # colocar a separação dos quartos nos gráficos
    quartos = quartos_do_jogo(df)

    # Análise da Posse de Bola dos times
    posse_bola = df[(df['Indicador'] == '3_Pts_C') | (df['Indicador'] == '3_Pts_T') |
                    (df['Indicador'] == '2_Pts_C') | (df['Indicador'] == '2_Pts_T') |
                    (df['Indicador'] == 'LL_Pts_C') | (df['Indicador'] == 'LL_Pts_T') |
                    (df['Indicador'] == 'ER') | (df['Indicador'] == 'FC_O') |
                    (df['Indicador'] == 'EN') | (df['Indicador'] == 'fim_partida')]

    # estamos invertendo os valores para deixar parecido com o jogo
    posse_bola = posse_bola[::-1]
    posse_bola.reset_index(drop=True, inplace=True)

    # Formula que descobre a posse de bola de cada time
    df_time_a, df_time_b = resultado_da_posse_de_bola(posse_bola, sigla_time_a, sigla_time_b)

    # Formula que junta as posses de bolas de cada time
    posse_de_bola = juntar_posses(df_time_a, df_time_b)

    # Análises da posse de bola
    lu_time_a = posse_de_bola
    lu_time_a['Time_Novo'] = 0

    for x in range(len(posse_de_bola)):
        if lu_time_a['Time'][x] == sigla_time_a:
            lu_time_a.loc[x, 'Time_Novo'] = lu_time_a['Tempo'][x]
        else:
            pass

    grafico_posse_time1 = lu_time_a
    grafico_posse_time1.reset_index(inplace=True)

    x = grafico_posse_time1['index']
    my_xticks = x
    frequency = 10


