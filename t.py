import pandas as pd
import os


ANOS = [20]

for k in ANOS:
    path_jogada = fr'C:/Users/Elen- PC/PycharmProjects/untitled1/Dados01/temporada 20{k}'
    files_jogada = os.listdir(path_jogada)
    files_jogada_csv = [path_jogada + '\\' + f for f in files_jogada if f[-3:] == 'csv']

    path_tabela = fr'C:/Users/Elen- PC/PycharmProjects/untitled1/Dados/temporada 20{k}'
    files_tabela = os.listdir(path_tabela)
    files_tabela_csv = [path_tabela + '\\' + f for f in files_tabela if f[-3:] == 'csv']

    aaa = 1
    for f in files_tabela_csv:
        print(f'Número da partida {aaa}')
        aaa += 1
        arquivo_time = f.replace(f'C:/Users/Elen- PC/PycharmProjects/untitled1/Dados/temporada 20{k}', '')
        print(arquivo_time)

        tabela_times['Data'] = ['nan', 'nan']
        tabela_times['Semana'] = ['nan', 'nan']
        tabela_times['Classificatoria/Playoffs'] = ['nan', 'nan']
        ########################################################################################################
        for j in files_tabela_csv:
            arquivo_tabela_time = j.replace(f'C:/Users/Elen- PC/PycharmProjects/untitled1/Dados/temporada 20{k}', '')
            if arquivo_time == arquivo_tabela_time:
                print('sim')
                df_tabela = pd.read_csv(j)
                tabela_times['Data'] = [df_tabela['Data'][1], df_tabela['Data'][1]]
                tabela_times['Semana'] = [df_tabela['Semana'][1], df_tabela['Semana'][1]]
                tabela_times['Classificatoria/Playoffs'] = [df_tabela['Classificatoria/Playoffs'][1],
                                                            df_tabela['Classificatoria/Playoffs'][1]]
            else:
                pass

