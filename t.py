import pandas as pd
import os


ANOS = [20]

for k in ANOS:
    path_jogada = fr'C:/Users/Elen- PC/PycharmProjects/untitled1/Dados01/temporada 20{k}'
    files_jogada = os.listdir(path_jogada)
    files_jogada_csv = [path_jogada + '\\' + f for f in files_jogada if f[-3:] == 'csv']
    # Aquivos desnecessários para a análise
    tirar = {path_jogada + fr'\falha_20{k}.csv', path_jogada + fr'\funcionando_20{k}.csv',
             path_jogada + fr'\Total_de_acao_acao_20{k}.csv'}
    files_csv = [elem for elem in files_jogada_csv if elem not in tirar]
    # files_csv = [elem.replace(path_jogada + '\\', '') for elem in files_csv]
    files_csv.sort(key=lambda _: int(_.split('_')[1]))
    print(files_csv)

    path_tabela = fr'C:/Users/Elen- PC/PycharmProjects/untitled1/Dados/temporada 20{k}'
    files_tabela = os.listdir(path_tabela)
    files_tabela_csv = [path_tabela + '\\' + f for f in files_tabela if f[-3:] == 'csv']

