from collections import Counter
import pandas as pd
import math
import numpy as np
from matplotlib import pyplot as plt

dados = pd.read_csv("Tabela_geral_2019_nova.csv")
UNIFACISA = dados.query("Time == 'UNIFACISA'").reset_index(drop=True)
Sao_Paulo = dados.query("Time == 'São Paulo'")
Pinheiros = dados.query("Time == 'Pinheiros'")
Brasilia = dados.query("Time == 'Brasília'")
Corinthians = dados.query("Time == 'Corinthians'")
Minas = dados.query("Time == 'Minas'")
Sesi_Franca = dados.query("Time == 'Sesi Franca'")
Bauru = dados.query("Time == 'Bauru'")
Sao_Jose = dados.query("Time == 'São José'")
Mogi = dados.query("Time == 'Mogi'")
Rio_Claro = dados.query("Time == 'Rio Claro'")
Paulistano = dados.query("Time == 'Paulistano'")
Pato_Basquete = dados.query("Time == 'Pato Basquete'")
Basq_Cearense = dados.query("Time == 'Basq. Cearense'")
Botafogo = dados.query("Time == 'Botafogo'")
Flamengo = dados.query("Time == 'Flamengo'")

# cada partida de cada time
jogo_UNIFACISA = UNIFACISA.query("Jogador == 'Equipe'").reset_index(drop=True)
jogo_Sao_Paulo = Sao_Paulo.query("Jogador == 'Equipe'")
jogo_Pinheiros = Pinheiros.query("Jogador == 'Equipe'")
jogo_Brasilia = Brasilia.query("Jogador == 'Equipe'")
jogo_Corinthians = Corinthians.query("Jogador == 'Equipe'")
jogo_Minas = Minas.query("Jogador == 'Equipe'")
jogo_Sesi_Franca = Sesi_Franca.query("Jogador == 'Equipe'")
jogo_Bauru = Bauru.query("Jogador == 'Equipe'")
jogo_Sao_Jose = Sao_Jose.query("Jogador == 'Equipe'")
jogo_Mogi = Mogi.query("Jogador == 'Equipe'")
jogo_Rio_Claro = Rio_Claro.query("Jogador == 'Equipe'")
jogo_Paulistano = Paulistano.query("Jogador == 'Equipe'")
jogo_Pato_Basquete = Pato_Basquete.query("Jogador == 'Equipe'")
jogo_Basq_Cearense = Basq_Cearense.query("Jogador == 'Equipe'")
jogo_Botafogo = Botafogo.query("Jogador == 'Equipe'")
jogo_Flamengo = Flamengo.query("Jogador == 'Equipe'")


# qual a frequencia dos jogadores nos jogos?
quantidade_jogadores = Counter(UNIFACISA['Jogador'])

# qual a frequencia relativa do número de jogadores em cada Equipe
fr_time_jogadores = Counter(jogo_UNIFACISA['Njogador'])
# print(fr_time_jogadores)

# qual a frequencia relativa do número de jogadores em cada jogo
geral = dados.query("Jogador == 'Equipe'")
fr_geral = Counter(geral['Njogador'])
soma = sum(fr_geral.values())
fr = [elem/soma for elem in fr_geral.values()]


# frequencia relativa dos indicadores de cada atleta do time
nome_jogadores = UNIFACISA['Jogador'].unique()

jogador = dados.loc[dados['Jogador'] == 'Barnes']
soma_jogador = jogador.sum(axis=0, numeric_only=True)

grupo = UNIFACISA.groupby('Jogador').sum()
print(grupo)

# fazer um histograma para cada indicador técnico
variavel = jogo_UNIFACISA['Pts_C']

NC = 6
max(variavel)
min(variavel)
amplitude = (max(variavel)-min(variavel))/NC
amplitude = math.ceil(amplitude)  # teto da amplitude


LI = min(variavel) - 0.5
LS = LI + amplitude*NC + 0.5

intervalo = list(np.arange(LI, LS, amplitude))

hist, bins = np.histogram(variavel, intervalo)

plt.hist(variavel, bins)
# plt.show()


"""
atleta_Georginho = dados.query("Jogador=='Georginho'").reset_index(drop=True)
Da para fazer alguns gráficos sobre isso
"""
