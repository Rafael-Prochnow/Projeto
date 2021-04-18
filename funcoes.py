import re
import datetime as dt
import pandas as pd
import numpy as np


# corresponde as siglas de cada jogo


def siglas(nome_time, temporada):
    if nome_time == 'Bauru':
        return 'BAU'

    elif nome_time == 'Mogi':
        return 'MOG'

    elif nome_time == 'VipTech CMB':
        return 'CMO'

    elif (nome_time == 'Brasília') & (temporada == '2020'):
        return 'BSB'
    elif (nome_time == 'Brasília') & (temporada == '2019'):
        return 'BSB'
    elif (nome_time == 'Brasília') & (temporada == '2018'):
        return 'BRA'

    elif nome_time == 'Paulistano':
        return 'CAP'

    elif nome_time == 'Flamengo':
        return 'FLA'

    elif nome_time == 'Minas':
        return 'MIN'

    elif nome_time == 'UNIFACISA':
        return 'UFC'

    elif nome_time == 'Cerrado Basquete':
        return 'CER'

    elif nome_time == 'Sesi Franca':
        return 'FRA'

    elif nome_time == 'Corinthians':
        return 'COR'

    elif nome_time == 'Pinheiros':
        return 'PIN'

    elif (nome_time == 'Fortaleza B') & (temporada == '2020'):
        return 'FOR'
    elif (nome_time == 'Fortaleza B') & (temporada == '2019'):
        return 'CEA'
    elif (nome_time == 'Fortaleza B') & (temporada == '2018'):
        return 'CEA'
    elif (nome_time == 'Fortaleza B') & (temporada == '2017'):
        return 'CEA'

    elif nome_time == 'KTO Caxias do Sul':
        return 'CAX'

    elif nome_time == 'Pato Basquete':
        return 'PAT'

    elif nome_time == 'São Paulo':
        return 'SPF'
    #####################################
    elif nome_time == 'Rio Claro':
        return 'RCB'
    elif nome_time == 'São José':
        return 'SJO'
    elif nome_time == 'Botafogo':
        return 'BOT'
    elif nome_time == 'Vasco da Gama':
        return 'VAS'
    elif nome_time == 'Joinville   AABJ ':
        return 'JLE'
    #######################################################
    elif nome_time == 'Vitória':
        return 'VIT'
    elif nome_time == 'L Sorocabana':
        return 'LSB'
    elif nome_time == 'Caxias do Sul':
        return 'CAX'


def limpeza_tempo(df):
    # Limpeza dos dados
    df.dropna(subset=['Tempo'], inplace=True)
    mudar_hora = []
    for x in df['Tempo']:
        if re.findall(r'..:..', x):
            mudar_hora.append(x)
        else:
            if re.findall(r'....', x):
                x = x[0:2] + ':' + x[2:4]
                mudar_hora.append(x)
            elif re.findall(r'...', x):
                x = '0' + x[0] + ':' + x[1:3]
                mudar_hora.append(x)
            elif re.findall(r'..', x):
                x = '00:' + x
                mudar_hora.append(x)
            elif re.findall(r'.', x):
                x = '00:0' + x
                mudar_hora.append(x)

    df['Tempo_2'] = mudar_hora
    df.drop('Tempo', axis=1, inplace=True)
    df['Tempo_2'] = df['Tempo_2'].apply(lambda x1: dt.datetime.strptime(x1, '%M:%S'))
    df['Tempo_2'] = df['Tempo_2'].apply(lambda x2: dt.time(x2.hour, x2.minute, x2.second))
    df['Tempo_2'] = df['Tempo_2'].apply(lambda x3: (x3.hour * 60 + x3.minute) * 60 + x3.second)
    # transforma os dados para números inteiros
    df['Quarto'] = df['Quarto'].apply(lambda l: int(l))
    return df


def transformar_segundos(df):
    # modificar o tempo decrescente para crescente (* -1)
    # acrescentar o tempo de cada quarto (primeiro quarto termina em 600s, o segundo quarto 2*600 = 1200 ...)
    tempo_novo = []
    for x, y in zip(df['Quarto'], df['Tempo_2']):
        if x == 1:
            a = (y - (600 * 1)) * -1
            tempo_novo.append(a)
        elif x == 2:
            a = (y - (600 * 2)) * -1
            tempo_novo.append(a)
        elif x == 3:
            a = (y - (600 * 3)) * -1
            tempo_novo.append(a)
        elif x == 4:
            a = (y - (600 * 4)) * -1
            tempo_novo.append(a)
        elif x == 5:
            a = (y - (600 * 4.5)) * -1
            tempo_novo.append(a)
        elif x == 6:
            a = (y - (600 * 5)) * -1
            tempo_novo.append(a)
        elif x == 7:
            a = (y - (600 * 5.5)) * -1
            tempo_novo.append(a)

    df['Tempo'] = tempo_novo
    df.drop('Tempo_2', axis=1, inplace=True)
    # deixando o DataFrame nessa ordem de colunas
    return df[['Quarto', 'Tempo', 'placar_casa', 'placar_visitante', 'Time', 'Indicador', 'Nome']]


def quartos_do_jogo(df):
    # colocar a separação dos quartos nos gráficos
    quartos_duplicados = df['Quarto'].unique()
    if len(quartos_duplicados) == 4:
        lista = [600, 1200, 1800, 2400]
        return lista
    elif len(quartos_duplicados) == 5:
        lista = [600, 1200, 1800, 2400, 2700]
        return lista
    elif len(quartos_duplicados) == 6:
        lista = [600, 1200, 1800, 2400, 2700, 3000]
        return lista
    elif len(quartos_duplicados) == 7:
        lista = [600, 1200, 1800, 2400, 2700, 3300]
        return lista


def resultado_da_posse_de_bola(posse_bola, sigla_time_a, sigla_time_b):
    lstime_b = [[]]
    lstime_a = [[]]
    for a in posse_bola.itertuples():
        if a.Time not in [sigla_time_b]:
            idx = a.Index - 1
            if idx >= 0:
                cc = posse_bola.loc[idx]
                lss = [
                    cc.Time,
                    cc.Tempo,
                    cc.Indicador,
                    cc.diferenca_placar_casa,
                    cc.diferenca_placar_visitante,
                    cc.diferenca_placar_absoluto
                ]
                lstime_b.append(lss)
            else:
                pass

        if a.Time not in [sigla_time_a]:
            idx = a.Index - 1
            if idx >= 0:
                cc = posse_bola.loc[idx]
                lss = [
                    cc.Time,
                    cc.Tempo,
                    cc.Indicador,
                    cc.diferenca_placar_casa,
                    cc.diferenca_placar_visitante,
                    cc.diferenca_placar_absoluto
                ]
                lstime_a.append(lss)
            else:
                pass

    df_time_b = pd.DataFrame(
        lstime_b, columns=["Time", "Tempo", "Indicador", "dif_casa", "dif_visita", "dif_abs"])

    df_time_b.dropna(how="any", inplace=True, axis="index")
    df_time_b = df_time_b[df_time_b.Time.str.contains(sigla_time_b)]

    df_time_a = pd.DataFrame(
        lstime_a, columns=["Time", "Tempo", "Indicador", "dif_casa", "dif_visita", "dif_abs"])

    df_time_a.dropna(how="any", inplace=True, axis="index")
    df_time_a = df_time_a[df_time_a.Time.str.contains(sigla_time_a)]
    return df_time_a, df_time_b


def juntar_posses(df_time_a, df_time_b):
    resultado = pd.concat([df_time_b, df_time_a], ignore_index=True)
    resultado.sort_values(by="Tempo", inplace=True)
    resultado.reset_index(inplace=True, drop=True)
    resultado["Tempo_Fim"] = resultado["Tempo"]
    tempo = resultado["Tempo"].diff()
    tempo.loc[0] = resultado["Tempo"].loc[0]
    resultado["Tempo"] = tempo
    return resultado


def acrescentar_indicadores(contagem):
    # Esses indicadores podem não aparecer no jogo
    # dessa maneira eu vou criar um if e acrescentar
    valores_coluna = []
    for i in contagem:
        valores_coluna.append(i)

    if 'EN' not in valores_coluna:
        contagem['EN'] = [0.0, 0.0]
    if 'LL_Pts_T' not in valores_coluna:
        contagem['LL_Pts_T'] = [0.0, 0.0]
    if 'LL_Pts_C' not in valores_coluna:
        contagem['LL_Pts_C'] = [0.0, 0.0]
    # substituir os valores NAN por 0(zero)
    contagem.fillna(0, inplace=True)
    return contagem


def par_impar(posse_bola):
    # precisamos fazer dois estilos de DataFrame
    # par = não influência no time que teve a primeira posse de bola
    # par = influência no time que teve a segunda posse de bola
    # inpar = não influência no time que teve a segunda posse de bola
    # inpar = influência no time que teve a primeira posse de bola
    if len(posse_bola) % 2 == 0:
        # print(f"Par: {len(posse_bola)}")
        return posse_bola
    else:
        # print(f"Impar: {len(posse_bola)}")
        d = {"Time": [0], "Tempo": [0], "Indicador": [0], "dif_casa": [0], "dif_visita": [0], "dif_abs": [0],
             "Tempo_Fim": [0], "pontuacao": [0]}
        a = pd.DataFrame(data=d)
        a.pontuacao = a.pontuacao.astype('float64')
        posse_bola = pd.concat([posse_bola, a], ignore_index=True)
    return posse_bola


def periodo_potencial(posse_bola):
    # Verificação das posses de bola pulando dois em dois
    indx_potencial_periodo = []
    for i in range(0, len(posse_bola), 2):
        # ache onde teve vantagem na pontuação
        # Time A fez ponto, mas o time B não fez
        if (posse_bola.pontuacao[i] >= 2) & (posse_bola.pontuacao[i + 1] >= -1):
            indx_potencial_periodo.append(i)
        # ache onde teve pontuação dos dois times
        # Time A fez ponto e o time B fez ponto
        # Elimina a primeira posse de bola com essa condição
        elif i > 2:
            if (posse_bola.pontuacao[i] >= 2) & (posse_bola.pontuacao[i + 1] <= -1):
                # Caso encontre uma troca de pontuação, nós precisamos avaliar outro critério
                # Caso apareça no ataque anterior uma vantagem na pontuação. PEGUE!
                # Come essa função está avaliando o primeiro time que atacou,
                # o time ao realizar um ponto estará na frente do placar anterior
                if (posse_bola.pontuacao[i - 2] >= 2) & (posse_bola.pontuacao[i - 1] >= -1):
                    indx_potencial_periodo.append(i)
                else:
                    pass
        else:
            pass
    # para ajudar no passo de verificação na separação dos períodos positivos eu criei um break
    # o break consiste em acrescentando o valor zero (0) no final da lista
    indx_potencial_periodo.append(0)
    return indx_potencial_periodo


def identificardor_periodo_positivo(indx_potencial_periodo, posse_bola):
    # Primeiro passo é fazer a diferença entre cada periodo identificado
    dif = np.diff(indx_potencial_periodo)
    resultado = []
    periodo = []
    # Depois precisamos encontra quais apresentão ataques consecutivos (2)
    # localizados os ataques, vamos agrupar os indxs e geramos periodos
    for i, j in zip(dif, range(len(dif))):
        # print(i)
        if i == 2:
            resultado.append(indx_potencial_periodo[j])
            resultado.append(indx_potencial_periodo[j + 1])
        else:
            periodo.append(sorted(set(resultado)))
            resultado = []
    periodo_positivo = []
    # depois de agrupa-los, nós identificamos quem apresenta valores nos períodos
    for i in periodo:
        if any(i):
            # para que sejam considerados periodos positivos utilizamos uma pontuação maior que 4 pontos no período
            if sum(posse_bola.loc[i, 'pontuacao']) >= 4:
                periodo_positivo.append(i)
            else:
                pass
        else:
            pass
    # retorna os períodos positivos do time
    return periodo_positivo


def acrescentar_valores_gerais(Tabela_Geral_Time1, nome_time_casa, nome_time_fora, dia_do_jogo, casa, classificatoria):
    tabela_time1 = Tabela_Geral_Time1.groupby(['Nome', 'Indicador']).count()
    tabela_time1_pivot = tabela_time1.pivot_table(index='Indicador', columns=['Nome'], aggfunc=sum, fill_value=0).T

    valores_coluna_time1 = []
    for i in tabela_time1_pivot:
        valores_coluna_time1.append(i)

    tamanho_df_pivot = len(tabela_time1_pivot)
    if 'TO' not in valores_coluna_time1:
        toco = [0 for itens in range(tamanho_df_pivot)]
        tabela_time1_pivot['TO'] = toco
    if 'FC_O' not in valores_coluna_time1:
        fco = [0 for itens in range(tamanho_df_pivot)]
        tabela_time1_pivot['FC_O'] = fco
    if 'FC_T' not in valores_coluna_time1:
        fct = [0 for itens in range(tamanho_df_pivot)]
        tabela_time1_pivot['FC_T'] = fct
    if 'FC_A' not in valores_coluna_time1:
        fca = [0 for itens in range(tamanho_df_pivot)]
        tabela_time1_pivot['FC_A'] = fca
    if 'EN' not in valores_coluna_time1:
        en = [0 for itens in range(tamanho_df_pivot)]
        tabela_time1_pivot['EN'] = en
    if 'LL_Pts_C' not in valores_coluna_time1:
        llc = [0 for itens in range(tamanho_df_pivot)]
        tabela_time1_pivot['LL_Pts_C'] = llc
    if 'LL_Pts_T' not in valores_coluna_time1:
        llt = [0 for itens in range(tamanho_df_pivot)]
        tabela_time1_pivot['LL_Pts_T'] = llt

    nome_time_casa0 = [nome_time_casa for itens in range(tamanho_df_pivot)]
    tabela_time1_pivot['Time'] = nome_time_casa0

    nome_time_fora0 = [nome_time_fora for itens in range(tamanho_df_pivot)]
    tabela_time1_pivot['Oponente'] = nome_time_fora0

    dia_do_jogo0 = [dia_do_jogo for itens in range(tamanho_df_pivot)]
    tabela_time1_pivot['Data'] = dia_do_jogo0

    casa0 = [casa for itens in range(tamanho_df_pivot)]
    tabela_time1_pivot['Casa/Fora'] = casa0

    classificatoria0 = [classificatoria for itens in range(tamanho_df_pivot)]
    tabela_time1_pivot['Classificatoria/Playoffs'] = classificatoria0
    tabela_time1_pivot.reset_index(inplace=True)
    tabela_time1_pivot.drop(['level_0'], axis=1, inplace=True)
    return tabela_time1_pivot


def criando_dataframe_times(tabela_time1_pivot, nome_time_casa):
    Time1_Final = pd.DataFrame()
    Time1_Final['Time'] = tabela_time1_pivot['Time']
    Time1_Final['Oponente'] = tabela_time1_pivot['Oponente']
    Time1_Final['Data'] = tabela_time1_pivot['Data']
    Time1_Final['Casa/Fora'] = tabela_time1_pivot['Casa/Fora']
    Time1_Final['Classificatoria/Playoffs'] = tabela_time1_pivot['Classificatoria/Playoffs']
    Time1_Final['Nome'] = tabela_time1_pivot['Nome']
    Time1_Final['Pts_3_C'] = tabela_time1_pivot['3_Pts_C'] * 3
    Time1_Final['Pts_3_T'] = (tabela_time1_pivot['3_Pts_T'] + tabela_time1_pivot['3_Pts_C']) * 3
    Time1_Final['Pts_2_C'] = (tabela_time1_pivot['2_Pts_C'] + tabela_time1_pivot['EN']) * 2
    Time1_Final['Pts_2_T'] = (tabela_time1_pivot['2_Pts_T'] + tabela_time1_pivot['2_Pts_C'] + tabela_time1_pivot[
        'EN']) * 2
    Time1_Final['LL_C'] = tabela_time1_pivot['LL_Pts_C']
    Time1_Final['LL_T'] = tabela_time1_pivot['LL_Pts_T'] + tabela_time1_pivot['LL_Pts_C']
    Time1_Final['RO'] = tabela_time1_pivot['RO']
    Time1_Final['RD'] = tabela_time1_pivot['RD']
    Time1_Final['RT'] = tabela_time1_pivot['RO'] + tabela_time1_pivot['RD']
    Time1_Final['AS'] = tabela_time1_pivot['AS']
    Time1_Final['BR'] = tabela_time1_pivot['BR']
    Time1_Final['TO'] = tabela_time1_pivot['TO']
    Time1_Final['FC'] = tabela_time1_pivot['FC'] + tabela_time1_pivot['FC_T'] + tabela_time1_pivot['FC_O'] + \
                        tabela_time1_pivot['FC_A']
    Time1_Final['FR'] = tabela_time1_pivot['FR']
    Time1_Final['ER'] = tabela_time1_pivot['ER']
    Time1_Final['EN'] = tabela_time1_pivot['EN']
    Time1_Final['substituicao_entra'] = tabela_time1_pivot['substituicao_entra']
    Time1_Final['substituicao_sai'] = tabela_time1_pivot['substituicao_sai']

    Time1_Final['Ar_Pts_C'] = (Time1_Final['Pts_3_C'] / 3) + (Time1_Final['Pts_2_C'] / 2) - (
                Time1_Final['EN'] / 2)  # por o teste3['Pts_2_C'] contabiliza EN
    Time1_Final['Ar_Pts_T'] = (Time1_Final['Pts_3_T'] / 3) + (Time1_Final['Pts_2_T'] / 2)  # NÃO contabiliza EN
    Time1_Final['Pts_C'] = (Time1_Final['Pts_3_C'] / 3) + (Time1_Final['Pts_2_C'] / 2) + Time1_Final['LL_C']
    Time1_Final['Pts_T'] = (Time1_Final['Pts_3_T'] / 3) + (Time1_Final['Pts_2_T'] / 2) + Time1_Final['LL_T']
    # mudar os nomes para ações coletivas
    Time1_Final = Time1_Final[(Time1_Final['Nome'] != nome_time_casa)]
    Time1_Final['posse_de_bola_Oliver'] = round(
        Time1_Final['Ar_Pts_T'] - Time1_Final['RO'] + Time1_Final['ER'] + (0.4 * Time1_Final['LL_T']), 0)
    return Time1_Final


def criando_analise_avancada_times(Tabela_Final):
    analise = pd.DataFrame()
    analise['Time'] = Tabela_Final['Time']
    analise['Oponente'] = Tabela_Final['Oponente']
    analise['Data'] = Tabela_Final['Data']
    analise['Casa/Fora'] = Tabela_Final['Casa/Fora']
    analise['Classificatoria/Playoffs'] = Tabela_Final['Classificatoria/Playoffs']
    analise['Nome'] = Tabela_Final['Nome']  # Jogadores
    analise['EF_Pts'] = round(Tabela_Final['Pts_C'] / Tabela_Final['Pts_T'], 3)  # eficiência dos pontos totais
    analise['FR_3_Pts_C'] = round((Tabela_Final['Pts_3_C'] * 3) / Tabela_Final['Pts_C'],
                                  3)  # frequência relativa do 3 pontos convertidos
    analise['FR_3_Pts_T'] = round((Tabela_Final['Pts_3_T'] * 3) / Tabela_Final['Pts_T'],
                                  3)  # frequência relativa do 3 pontos tentados
    analise['EF_Pts_3'] = round(Tabela_Final['Pts_3_C'] / Tabela_Final['Pts_3_T'], 3)  # eficiência dos 3 pontos
    analise['FR_2_Pts_C'] = round((Tabela_Final['Pts_2_C'] * 2) / Tabela_Final['Pts_C'],
                                  3)  # frequência relativa do 2 pontos convertidos
    analise['FR_2_Pts_T'] = round((Tabela_Final['Pts_2_T'] * 2) / Tabela_Final['Pts_T'],
                                  3)  # frequência relativa do 2 pontos tentados
    analise['EF_Pts_2'] = round(Tabela_Final['Pts_2_C'] / Tabela_Final['Pts_2_T'], 3)  # eficiência dos 2 pontos
    analise['FR_LL_C'] = round(Tabela_Final['LL_C'] / Tabela_Final['Pts_C'],
                               3)  # frequência relativa dos Lances Livres convertidos
    analise['FR_LL_T'] = round(Tabela_Final['LL_T'] / Tabela_Final['Pts_T'],
                               3)  # frequência relativa dos Lances Livres tentados
    analise['EF_LL'] = round(Tabela_Final['LL_C'] / Tabela_Final['LL_T'], 3)  # eficiência dos Lances Livres
    # analise['Pace']
    # four fectores
    analise['eFG_%'] = round((Tabela_Final['Ar_Pts_C'] + 0.5 * Tabela_Final['Pts_3_C']) / Tabela_Final['Ar_Pts_T'],
                             3)  # aproveitamento efetivo
    analise['TOV_%'] = round(
        100 * Tabela_Final['ER'] / (Tabela_Final['Ar_Pts_T'] + 0.475 * Tabela_Final['LL_T'] + Tabela_Final['ER']),
        1)  # fator turnover
    analise['FTA/FGA'] = round(Tabela_Final['LL_T'] / Tabela_Final['Ar_Pts_C'],
                               3)  # fator de aproveitamento dos lances livres
    # analise['ORB%'] =  # precisa do resultado do time adv

    analise['Posse_de_Bola'] = Tabela_Final['posse_de_bola']  # posse de bola
    analise['Offensive_Rating'] = 100 * round(Tabela_Final['Pts_C'] / Tabela_Final['posse_de_bola'],
                                              3)  # pontos por posse de bola com o ajusto de 100 posses

    analise['TS_%'] = round(Tabela_Final['Pts_C'] / (2 * (Tabela_Final['Ar_Pts_T'] + 0.475 * Tabela_Final['LL_T'])),
                            3)  # porcentagem dos arremessos
    analise['Ass/ER'] = round(Tabela_Final['AS'] / Tabela_Final['ER'], 3)  # assistência por erros
    analise['AS_Ratio'] = 100 * round((Tabela_Final['AS'] / Tabela_Final['posse_de_bola']),
                                      3)  # assistências por posse de bola
    analise.reset_index(drop=True, inplace=True)
    return analise



