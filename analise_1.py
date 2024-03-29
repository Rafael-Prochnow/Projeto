import pandas as pd
import os
from datetime import datetime
import re
from funcoes import siglas, limpeza_tempo, transformar_segundos, quartos_do_jogo, resultado_da_posse_de_bola, \
    juntar_posses, acrescentar_indicadores, par_impar, periodo_potencial, identificardor_periodo_positivo, \
    acrescentar_valores_gerais, criando_dataframe_times

# ANOS = [20, 19, 18, 17, 16, 15, 14, 13]
ANOS = [17]
aprendizado = pd.DataFrame([])

for k in ANOS:
    # Localizando na pasta os jogos contendo Jogada-Jogada do NBB retirados do Web Scraping
    path = fr'C:/Users/Elen- PC/PycharmProjects/untitled1/Dados01/temporada 20{k}'
    files = os.listdir(path)
    files_csv = [path + '\\' + f for f in files if f[-3:] == 'csv']
    # Aquivos desnecessários para a análise
    tirar = {path + fr'\falha_20{k}.csv', path + fr'\funcionando_20{k}.csv',
             path + fr'\Total_de_acao_acao_20{k}.csv'}
    files_csv = [_ for _ in files_csv if _ not in tirar]
    files_csv.sort(key=lambda _: int(_.split('_')[1]))

    # Localizando na pasta os jogos contendo a Tabela do NBB retirados do Web Scraping
    path_tabela = fr'C:/Users/Elen- PC/PycharmProjects/untitled1/Dados/temporada 20{k}'
    files_tabela = os.listdir(path_tabela)
    files_tabela_csv = [path_tabela + '\\' + f for f in files_tabela if f[-3:] == 'csv']
    # Arquivos desnecessários para a análise
    tirar_tabela = {path_tabela + fr'\falha_20{k}.csv', path_tabela + fr'\funcionando_20{k}.csv',
                    path_tabela + fr'\Total_de_Tabela_20{k}.csv'}
    files_tabela_csv = [elem for elem in files_tabela_csv if elem not in tirar_tabela]

    aaa = 1
    for f in files_csv:
        # print(f'Número da partida {aaa}')
        aaa += 1
        print(f)
        df = pd.read_csv(f)
        arquivo_time = f.replace(path + '\\', '')
        print(arquivo_time)
        expressao_regular = re.findall(r'[A-Z].*?[.]', arquivo_time)[0]
        expressao_regular = str(expressao_regular).strip("['.']").split('_x_')
        nome_time_casa = expressao_regular[0]
        nome_time_fora = expressao_regular[1]

        # Informações do jogo
        data_hoje = datetime.today().strftime('%d/%m/%Y')
        dia_do_jogo = f'{aaa}/01/20{k}'
        temporada = f'20{k}'
        sigla_time_a = siglas(nome_time_casa)
        sigla_time_b = siglas(nome_time_fora)
        casa = 'casa'
        fora = 'fora'
        classificatoria = '1 Turno'
        ############################################################################################
        # Limpeza dos dados
        df = limpeza_tempo(df)

        # modificar o tempo decrescente para crescente (* -1)
        # acrescentar o tempo de cada quarto (primeiro quarto termina em 600s, o segundo quarto 2*600 = 1200 ...)
        df = transformar_segundos(df)

        # Acrescentado colunas: diferenca_placar_casa e diferenca_placar_visitante
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

        #Gráfico 1

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

        #Gráfico 2

        lu_time_b = posse_de_bola
        lu_time_b['Time_Novo'] = 0

        for x in range(len(posse_de_bola)):
            if lu_time_b['Time'][x] == sigla_time_b:
                lu_time_b.loc[x, 'Time_Novo'] = lu_time_b['Tempo'][x]
            else:
                pass

        grafico_posse_time2 = lu_time_b
        grafico_posse_time2.reset_index(inplace=True)
        x2 = grafico_posse_time2['index']
        my_xticks2 = x2
        frequency2 = 10

        #Gráfico 3

        # Análises descritiva da posse de bola

        soma_a = df_time_a['Indicador'].value_counts().sum()
        soma_b = df_time_b['Indicador'].value_counts().sum()

        contagem = pd.DataFrame()
        contagem = contagem.append(df_time_a['Indicador'].value_counts(), ignore_index=True)
        contagem = contagem.append(df_time_b['Indicador'].value_counts(), ignore_index=True)

        # Esses indicadores podem não aparecer no jogo
        # dessa maneira eu vou criar um if e acrescentar
        contagem = acrescentar_indicadores(contagem)

        contagem.loc[0, '2_Pts_C'] = contagem['2_Pts_C'][0] + contagem['EN'][0]
        contagem.loc[1, '2_Pts_C'] = contagem['2_Pts_C'][1] + contagem['EN'][1]
        contagem.drop('EN', inplace=True, axis=1)
        contagem.rename(columns={"2_Pts_T": "2_Pts_E", "3_Pts_T": "3_Pts_E", "LL_Pts_T": "LL_Pts_E"}, inplace=True)

        contagem['2_Pts_T'] = contagem['2_Pts_C'] + contagem['2_Pts_E']
        contagem['3_Pts_T'] = contagem['3_Pts_C'] + contagem['3_Pts_E']
        contagem['LL_Pts_T'] = contagem['LL_Pts_C'] + contagem['LL_Pts_E']
        contagem['Time'] = [sigla_time_a, sigla_time_b]
        contagem['posse'] = [soma_a, soma_b]
        contagem['%2_Pts_C'] = [round((contagem['2_Pts_C'][0] / soma_a) * 100),
                                round((contagem['2_Pts_C'][1] / soma_b) * 100)]
        contagem['%2_Pts_E'] = [round((contagem['2_Pts_E'][0] / soma_a) * 100),
                                round((contagem['2_Pts_E'][1] / soma_b) * 100)]
        contagem['%3_Pts_C'] = [round((contagem['3_Pts_C'][0] / soma_a) * 100),
                                round((contagem['3_Pts_C'][1] / soma_b) * 100)]
        contagem['%3_Pts_E'] = [round((contagem['3_Pts_E'][0] / soma_a) * 100),
                                round((contagem['3_Pts_E'][1] / soma_b) * 100)]
        contagem['%LL_Pts_C'] = [round((contagem['LL_Pts_C'][0] / soma_a) * 100),
                                 round((contagem['LL_Pts_C'][1] / soma_b) * 100)]
        contagem['%LL_Pts_E'] = [round((contagem['LL_Pts_E'][0] / soma_a) * 100),
                                 round((contagem['LL_Pts_E'][1] / soma_b) * 100)]
        contagem['Tempo_de_posse'] = [
            (round(posse_de_bola.loc[posse_de_bola['Time'] == sigla_time_a].Tempo.sum() / 60)),
            (round(posse_de_bola.loc[posse_de_bola['Time'] == sigla_time_b].Tempo.sum() / 60))]
        contagem['Ataques/min'] = [(round(contagem['posse'][0] / contagem['Tempo_de_posse'][0], 2)),
                                   (round(contagem['posse'][1] / contagem['Tempo_de_posse'][1], 2))]

        contagem = contagem[['Time', 'posse', 'Tempo_de_posse', 'Ataques/min',
                             '2_Pts_C', '2_Pts_E', '2_Pts_T',
                             '3_Pts_C', '3_Pts_E', '3_Pts_T',
                             'LL_Pts_C', 'LL_Pts_E', 'LL_Pts_T',
                             '%2_Pts_C', '%2_Pts_E', '%3_Pts_C',
                             '%3_Pts_E', '%LL_Pts_C', '%LL_Pts_E']]

        posse_de_bola_a = posse_de_bola[posse_de_bola['Time'] == sigla_time_a]
        v1 = len(posse_de_bola_a[posse_de_bola_a['Tempo'] <= 5])
        v2 = len(posse_de_bola_a[(posse_de_bola_a['Tempo'] > 5) & (posse_de_bola_a['Tempo'] <= 10)])
        v3 = len(posse_de_bola_a[(posse_de_bola_a['Tempo'] > 10) & (posse_de_bola_a['Tempo'] <= 14)])
        v4 = len(posse_de_bola_a[(posse_de_bola_a['Tempo'] > 14) & (posse_de_bola_a['Tempo'] <= 24)])
        v5 = len(posse_de_bola_a[posse_de_bola_a['Tempo'] > 24])
        valores_a = {f'{sigla_time_a}': (v1, v2, v3, v4, v5)}

        posse_de_bola_b = posse_de_bola[posse_de_bola['Time'] == sigla_time_b]
        v1 = len(posse_de_bola_b[posse_de_bola_b['Tempo'] <= 5])
        v2 = len(posse_de_bola_b[(posse_de_bola_b['Tempo'] > 5) & (posse_de_bola_b['Tempo'] <= 10)])
        v3 = len(posse_de_bola_b[(posse_de_bola_b['Tempo'] > 10) & (posse_de_bola_b['Tempo'] <= 14)])
        v4 = len(posse_de_bola_b[(posse_de_bola_b['Tempo'] > 14) & (posse_de_bola_b['Tempo'] <= 24)])
        v5 = len(posse_de_bola_b[posse_de_bola_b['Tempo'] > 24])
        valores_b = {f'{sigla_time_b}': (v1, v2, v3, v4, v5)}

        # tempo de ataque separado por cada ataque
        # juntar valores de A e valores de B
        valores_a.update(valores_b)
        tempos = ('<=5', '>5<=10', '>10<=14', '>14<=24', '>24')
        ataques = pd.DataFrame(data=valores_a, index=tempos)

        #Gráfico 4

        # Analisar os períodos positivos dos times
        # Utilizando a diferença do placar entre casa e visitante, aplicando diff (diferença entre as linhas)
        # e usando seu valor absoluto (abs())
        # nós podemos encontrar o valor de cada indicador técnico
        posse_de_bola["pontuacao"] = posse_de_bola["dif_casa"].diff()
        posse_de_bola["pontuacao"] = posse_de_bola["pontuacao"].apply(lambda x4: abs(x4))
        # como o primeiro valor some quando fazemos a diff e esse primeiro valor é importante
        # pq é o primeiro ponto, nós adicionamos ele
        novo_valor = posse_de_bola["dif_casa"][0]
        posse_de_bola.loc[0, 'pontuacao'] = abs(novo_valor)
        # questão de precaução
        posse_de_bola.reset_index(inplace=True, drop=True)

        # dois tipos de posse de bola
        # 1 o time que teve a primeira posse de bola
        posse_bola_um = posse_de_bola.copy()

        # avaliar quem é o primeiro a ter a posse de bola para poder se encaixar com a função das posses
        segunda_posse = posse_de_bola.Time[1]

        # Perguntar para o thomaz pq está errado
        for i in range(len(posse_bola_um)):
            if posse_bola_um.Time[i] == segunda_posse:
                posse_bola_um.loc[i, 'pontuacao'] = posse_bola_um.pontuacao[i] * -1
            else:
                pass

        posse_bola_um = par_impar(posse_bola_um)

        indx_potencial_periodo = periodo_potencial(posse_bola_um)
        periodo_positivo = identificardor_periodo_positivo(indx_potencial_periodo, posse_bola_um)

        # Colocar nos gráficos os periodos
        # time A
        segmento = [[]]
        # Time B
        segmento_dois = [[]]

        # localizar o tempo de inicio e tempo final do periodo
        # No caso precisamos pegar o primeiro indx e subtrair por 1 (indx-1), assim podemos ter a posse completa
        # até a realização do ponto
        # Localizar o último indx que representa o final do período positivo
        if segunda_posse == sigla_time_a:
            positivo_inicio_time_b = []
            positivo_fim_time_b = []
            for i in periodo_positivo:
                if i[0] == 0:
                    positivo_inicio_time_b.append(posse_bola_um.loc[i[0], 'Tempo_Fim'])
                    positivo_fim_time_b.append(posse_bola_um.loc[i[len(i) - 1], 'Tempo_Fim'])
                    segmento_dois.append(
                        [posse_bola_um.loc[i[0], 'Tempo_Fim'], posse_bola_um.loc[i[len(i) - 1], 'Tempo_Fim']])
                else:
                    positivo_inicio_time_b.append(posse_bola_um.loc[i[0] - 1, 'Tempo_Fim'])
                    positivo_fim_time_b.append(posse_bola_um.loc[i[len(i) - 1], 'Tempo_Fim'])
                    segmento_dois.append(
                        [posse_bola_um.loc[i[0] - 1, 'Tempo_Fim'], posse_bola_um.loc[i[len(i) - 1], 'Tempo_Fim']])
        else:
            positivo_inicio_time_a = []
            positivo_fim_time_a = []
            for i in periodo_positivo:
                if i[0] == 0:
                    positivo_inicio_time_a.append(posse_bola_um.loc[i[0], 'Tempo_Fim'])
                    positivo_fim_time_a.append(posse_bola_um.loc[i[len(i) - 1], 'Tempo_Fim'])
                    segmento.append(
                        [posse_bola_um.loc[i[0], 'Tempo_Fim'], posse_bola_um.loc[i[len(i) - 1], 'Tempo_Fim']])
                else:
                    positivo_inicio_time_a.append(posse_bola_um.loc[i[0] - 1, 'Tempo_Fim'])
                    positivo_fim_time_a.append(posse_bola_um.loc[i[len(i) - 1], 'Tempo_Fim'])
                    segmento.append(
                        [posse_bola_um.loc[i[0] - 1, 'Tempo_Fim'], posse_bola_um.loc[i[len(i) - 1], 'Tempo_Fim']])

        # 2 o time que teve a segunda posse de bola
        posse_bola_dois = posse_de_bola.copy()
        posse_bola_dois.drop([0], inplace=True)
        posse_bola_dois.reset_index(drop=True, inplace=True)
        # avaliar quem é o primeiro a ter a posse de bola para poder se encaixar com a função das posses
        segunda_posse_dois = posse_bola_dois.Time[1]

        for i in range(len(posse_bola_dois)):
            if posse_bola_dois.Time[i] == segunda_posse_dois:
                posse_bola_dois.loc[i, 'pontuacao'] = posse_bola_dois.pontuacao[i] * -1
            else:
                pass

        posse_bola_dois = par_impar(posse_bola_dois)
        indx_potencial_periodo_dois = periodo_potencial(posse_bola_dois)
        periodo_positivo_dois = identificardor_periodo_positivo(indx_potencial_periodo_dois, posse_bola_dois)

        # localizar o tempo de inicio e tempo final do periodo
        # No caso precisamos pegar o primeiro indx e subtrair por 1 (indx-1), assim podemos ter a posse completa
        # até a realização do ponto
        # Localizar o último indx que representa o final do período positivo
        if segunda_posse_dois == sigla_time_a:
            positivo_inicio_time_b = []
            positivo_fim_time_b = []
            for i in periodo_positivo_dois:
                if i[0] == 0:
                    positivo_inicio_time_b.append(posse_bola_um.loc[i[0], 'Tempo_Fim'])
                    positivo_fim_time_b.append(posse_bola_dois.loc[i[len(i) - 1], 'Tempo_Fim'])
                    segmento_dois.append(
                        [posse_bola_um.loc[i[0], 'Tempo_Fim'], posse_bola_dois.loc[i[len(i) - 1], 'Tempo_Fim']])
                else:
                    positivo_inicio_time_b.append(posse_bola_dois.loc[i[0] - 1, 'Tempo_Fim'])
                    positivo_fim_time_b.append(posse_bola_dois.loc[i[len(i) - 1], 'Tempo_Fim'])
                    segmento_dois.append(
                        [posse_bola_dois.loc[i[0] - 1, 'Tempo_Fim'], posse_bola_dois.loc[i[len(i) - 1], 'Tempo_Fim']])
            # print('Time B')
            # print(positivo_inicio_time_b)
            # print(positivo_fim_time_b)
        else:
            positivo_inicio_time_a = []
            positivo_fim_time_a = []
            for i in periodo_positivo_dois:
                if i[0] == 0:
                    positivo_inicio_time_a.append(posse_bola_um.loc[i[0], 'Tempo_Fim'])
                    positivo_fim_time_a.append(posse_bola_dois.loc[i[len(i) - 1], 'Tempo_Fim'])
                    segmento.append(
                        [posse_bola_um.loc[i[0], 'Tempo_Fim'], posse_bola_dois.loc[i[len(i) - 1], 'Tempo_Fim']])
                else:
                    positivo_inicio_time_a.append(posse_bola_dois.loc[i[0] - 1, 'Tempo_Fim'])
                    positivo_fim_time_a.append(posse_bola_dois.loc[i[len(i) - 1], 'Tempo_Fim'])
                    segmento.append(
                        [posse_bola_dois.loc[i[0] - 1, 'Tempo_Fim'], posse_bola_dois.loc[i[len(i) - 1], 'Tempo_Fim']])

        # Time A
        del segmento[0]
        # Time B
        del segmento_dois[0]
        #################################################################################################
        # Tabela de dados gerais
        Tabela_Geral = df[['Time', 'Indicador', 'Nome']]
        Tabela_Geral_Time1 = Tabela_Geral[Tabela_Geral['Time'] == sigla_time_a]
        Tabela_Geral_Time2 = Tabela_Geral[Tabela_Geral['Time'] == sigla_time_b]

        # Esses indicadores podem não aparecer no jogo
        # dessa maneira eu vou criar um if e acrescentar

        tabela_time1_pivot = acrescentar_valores_gerais(Tabela_Geral_Time1, nome_time_casa, nome_time_fora,
                                                        dia_do_jogo, casa, classificatoria)
        # print(tabela_time1_pivot)

        tabela_time2_pivot = acrescentar_valores_gerais(Tabela_Geral_Time2, nome_time_fora, nome_time_casa,
                                                        dia_do_jogo, fora, classificatoria)

        # criar um novo data frame e agregar a soma
        Time1_Final = criando_dataframe_times(tabela_time1_pivot, nome_time_casa)

        Time2_Final = criando_dataframe_times(tabela_time2_pivot, nome_time_fora)

        # Somar tudo para ter o resultado da equipe
        resultado_Time1 = Time1_Final.sum()
        resultado_Time2 = Time2_Final.sum()
        resultado_Time1['Nome'] = 'Equipe'
        resultado_Time2['Nome'] = 'Equipe'
        resultado_Time1['Time'] = nome_time_casa
        resultado_Time2['Time'] = nome_time_fora
        resultado_Time1['Oponente'] = nome_time_fora
        resultado_Time2['Oponente'] = nome_time_casa
        resultado_Time1['Data'] = dia_do_jogo
        resultado_Time2['Data'] = dia_do_jogo
        resultado_Time1['Casa/Fora'] = casa
        resultado_Time2['Casa/Fora'] = fora
        resultado_Time1['Classificatoria/Playoffs'] = classificatoria
        resultado_Time2['Classificatoria/Playoffs'] = classificatoria
        # agregar no dataframe final
        Time1_Final = Time1_Final.append(resultado_Time1, ignore_index=True)
        Time2_Final = Time2_Final.append(resultado_Time2, ignore_index=True)
        Time1_Final['Ar_Pts_C'] = Time1_Final['Ar_Pts_C'].astype(int)
        Time1_Final['Ar_Pts_T'] = Time1_Final['Ar_Pts_T'].astype(int)
        Time2_Final['Ar_Pts_C'] = Time2_Final['Ar_Pts_C'].astype(int)
        Time2_Final['Ar_Pts_T'] = Time2_Final['Ar_Pts_T'].astype(int)

        # esse código é para a criação dos gráficos de comparação
        tabela_times = pd.concat([Time1_Final[Time1_Final['Nome'] == 'Equipe'],
                                  Time2_Final[Time2_Final['Nome'] == 'Equipe']], ignore_index=True)

        # Acrescentar a diferença do placar e vitória derrota
        dif_placar_geral = tabela_times['Pts_C'].diff()
        # acrescenta a diferença do placar do times
        positivo = []
        negativo = []
        resul_dif = []
        op_1 = ['vitória', 'derrota']
        op_2 = ['derrota', 'vitória']
        tamanho_df_pivot = len(Time1_Final)
        tamanho_df_pivot0 = len(Time2_Final)
        if dif_placar_geral[1] <= 0:
            positivo = abs(dif_placar_geral[1])
            negativo = dif_placar_geral[1]
            resul_dif = [positivo, negativo]
            tabela_times['Diferenca_Placar'] = resul_dif
            tabela_times['Vitoria/Derrota'] = op_1
            ################################################
            vit_der = ['vitória' for _ in range(tamanho_df_pivot)]
            Time1_Final['Vitoria/Derrota'] = vit_der
            dif = [positivo for _ in range(tamanho_df_pivot)]
            Time1_Final['Diferenca_Placar'] = dif
            #########################################################
            vit_der0 = ['derrota' for _ in range(tamanho_df_pivot0)]
            Time2_Final['Vitoria/Derrota'] = vit_der0
            dif0 = [negativo for _ in range(tamanho_df_pivot0)]
            Time2_Final['Diferenca_Placar'] = dif0
        else:
            positivo = dif_placar_geral[1]
            negativo = -(dif_placar_geral[1])
            resul_dif = [negativo, positivo]
            tabela_times['Diferenca_Placar'] = resul_dif
            tabela_times['Vitoria/Derrota'] = op_2
            ################################################
            vit_der = ['derrota' for itens in range(tamanho_df_pivot)]
            Time1_Final['Vitoria/Derrota'] = vit_der
            dif = [negativo for itens in range(tamanho_df_pivot)]
            Time1_Final['Diferenca_Placar'] = dif
            #########################################################
            vit_der0 = ['vitória' for itens in range(tamanho_df_pivot0)]
            Time2_Final['Vitoria/Derrota'] = vit_der0
            dif0 = [positivo for itens in range(tamanho_df_pivot0)]
            Time2_Final['Diferenca_Placar'] = dif0

        Tabela_Final = pd.concat([Time1_Final, Time2_Final]).reset_index(drop=True)
        # Acrescentar o valor de preriodos posítivo e negativo
        tabela_times['Periodos_Positivos'] = [len(segmento),
                                              len(segmento_dois)]
        tabela_times['posse_de_bola'] = [contagem['posse'][0],
                                         contagem['posse'][1]]

        tabela_times['Ataques/min'] = [contagem['Ataques/min'][0],
                                       contagem['Ataques/min'][1]]

        tabela_times['Tempo_de_posse'] = [contagem['Tempo_de_posse'][0],
                                          contagem['Tempo_de_posse'][1]]

        tabela_times['Data'] = ['nan', 'nan']
        tabela_times['Semana'] = ['nan', 'nan']
        tabela_times['Classificatoria/Playoffs'] = ['nan', 'nan']
        ########################################################################################################
        for j in files_tabela_csv:
            arquivo_tabela_time = j.replace(path_tabela + '\\', '')
            if arquivo_time == arquivo_tabela_time:
                print('sim')
                df_tabela = pd.read_csv(j)
                tabela_times['Data'] = [df_tabela['Data'][1], df_tabela['Data'][1]]
                tabela_times['Semana'] = [df_tabela['Semana'][1], df_tabela['Semana'][1]]
                tabela_times['Classificatoria/Playoffs'] = [df_tabela['Classificatoria/Playoffs'][1],
                                                            df_tabela['Classificatoria/Playoffs'][1]]
            else:
                pass
        # Dataframe para o Aprendizado
        aprendizado = aprendizado.append(tabela_times, ignore_index=True)
        ########################################################################################################
        # Análise Avançada
        # analise = criando_analise_avancada_times(Tabela_Final)
        ############################################################################################################

aprendizado.to_csv('ex.csv')
