import pandas as pd
import os
import numpy as np
import datetime as dt
from datetime import datetime
import re


def siglas(nome_time):
    if nome_time == 'Bauru':
        return 'BAU'

    elif nome_time == 'MOGI1':
        return 'MOG'

    elif nome_time == 'VipTech CMB':
        return 'CMO'

    elif nome_time == 'Brasília':
        return 'BRA'

    elif nome_time == 'Paulistano':
        return 'CAP'

    elif nome_time == 'Flamengo':
        return 'FLA'

    elif nome_time == 'Minas':
        return 'MIN'

    elif nome_time == 'UNIFACISA':
        return 'UFC'

    elif nome_time == 'Cerrado':
        return 'CER'

    elif nome_time == 'SESI Franca':
        return 'FRA'

    elif nome_time == 'Corinthians':
        return 'COR'

    elif nome_time == 'Pinheiros':
        return 'PIN'

    elif nome_time == 'Fortaleza B. C':
        return 'FOR'

    elif nome_time == 'KTO Caxias do Sul':
        return 'CAX'

    elif nome_time == 'Pato':
        return 'PAT'

    elif nome_time == 'São Paulo':
        return 'SPF'


# path = r'C:\Users\Elen- PC\Jupyter\teste'


'''files = os.listdir(path)
df = pd.DataFrame()
nome_time_casa = 'Bauru'
nome_time_fora = 'Corinthians'

files_csv = [path + '\\' + f for f in files if f[-3:] == 'csv']

for f in files_csv:
    data = pd.read_csv(f)
    df = df.append(data)'''


arquivo = "tabela_1_Flamengo_x_Brasília.csv"
df = pd.read_csv(f'C:/Users/Elen- PC/Jupyter/teste/{arquivo}')

expressao_regular = re.findall(r'[A-Z].*?[.]', arquivo)
expressao_regular = str(expressao_regular).strip('[]')
expressao_regular0 = expressao_regular.split('_x_')
casa = expressao_regular0[0]
nome_time_casa = casa.replace("'", "")

fora = expressao_regular0[1]
nome_time_fora = fora.replace(".'", "")

data_hoje = datetime.today().strftime('%d/%m/%Y')
dia_do_jogo = '02/01/2021'
temporada = 2019
sigla_time_a = siglas(nome_time_casa)
sigla_time_b = siglas(nome_time_fora)
casa = 'casa'
fora = 'fora'
classificatoria = '1 Turno'

df.dropna(subset=['Tempo'], inplace=True)

# Lipeza dos dados de tempo
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
df['Tempo_2'] = df['Tempo_2'].apply(lambda x: dt.datetime.strptime(x, '%M:%S'))
df['Tempo_2'] = df['Tempo_2'].apply(lambda x: dt.time(x.hour, x.minute, x.second))
df['Tempo_2'] = df['Tempo_2'].apply(lambda x: (x.hour * 60 + x.minute) * 60 + x.second)
# transforma os dados para números inteiros
df['Quarto'] = df['Quarto'].apply(lambda l: int(l))

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
df = df[['Quarto', 'Tempo', 'placar_casa', 'placar_visitante', 'Time', 'Indicador', 'Nome']]

# Acrescentando mais colunas
df['diferenca_placar_casa'] = df['placar_casa'] - df['placar_visitante']
df['diferenca_placar_visitante'] = df['placar_visitante'] - df['placar_casa']

# Analise da  pontuação dos times
pontuacao = df[(df['Indicador'] == '3_Pts_C') |
               (df['Indicador'] == '2_Pts_C') |
               (df['Indicador'] == 'LL_Pts_C') |
               (df['Indicador'] == 'EN') |
               (df['Indicador'] == 'fim_partida')]

# estamos invertendo os valores para deixar parecido com o jogo
pontuacao = pontuacao[::-1]
pontuacao.reset_index(drop=True, inplace=True)
quartos = [600, 1200, 1800, 2400]


# Análise da posse de bola dos times
posse_bola = df[(df['Indicador'] == '3_Pts_C') | (df['Indicador'] == '3_Pts_T') |
                (df['Indicador'] == '2_Pts_C') | (df['Indicador'] == '2_Pts_T') |
                (df['Indicador'] == 'LL_Pts_C') | (df['Indicador'] == 'LL_Pts_T') |
                (df['Indicador'] == 'ER') | (df['Indicador'] == 'FC_O') |
                (df['Indicador'] == 'EN') | (df['Indicador'] == 'fim_partida')]

# estamos invertendo os valores para deixar parecido com o jogo
posse_bola = posse_bola[::-1]
posse_bola.reset_index(drop=True, inplace=True)

# Utilizamos uma Flag para diferenciar as paradas entre os tempos iniciais de cada posse
flag = -1
# valores da ultima linha
ultima_linha = []
# valores finais da posse de bola
tempo_a_peridodo_final = []
tempo_b_peridodo_final = []
# identifica o tempo final
tempo_a_fim = 0
tempo_b_fim = 0

for i in range(len(posse_bola)):
    # caso corresponda ao nome do time A
    if posse_bola['Time'][i] == sigla_time_a:
        if flag != 1:
            # quando chegamos na flag o pensamento é pegar o primeiro valor que apresenta no Time A
            # o loop do Time B é terminado
            tempo_b_peridodo_final.append(tempo_b_fim)
            # pega o primeiro valor do tempo de início
            tempo_a_fim = posse_bola['Tempo'][i]
            flag = 1
        else:
            tempo_a_fim = posse_bola['Tempo'][i]
            flag = 1
    # caso corresponda ao nome do time B
    elif posse_bola['Time'][i] == sigla_time_b:
        if flag != 0:
            # quando chegamos na flag o pensamento é pegar o primeiro valor que apresenta no Time B
            # o loop do Time A é terminado
            tempo_a_peridodo_final.append(tempo_a_fim)
            # pega o primeiro valor do tempo final
            tempo_b_fim = posse_bola['Tempo'][i]
            flag = 0
        else:
            tempo_b_fim = posse_bola['Tempo'][i]
            flag = 0
    # caso corresponda ao termino da partida
    else:
        # caso chegue no final da linha os valores são armazenados
        ultima_linha = posse_bola['Tempo'][i]
        if flag != 1:
            tempo_b_peridodo_final.append(tempo_b_fim)
        else:
            tempo_a_peridodo_final.append(tempo_a_fim)

# caso o tamanho do inicio esteja variando  por causa dos ultimos lances relacionados ao tempo de partida
# a gente alinha dessa forma
if len(tempo_a_peridodo_final) < len(tempo_b_peridodo_final):
    # o fim do tempo b é o início do tempo A, pq a troca de bola é alternada
    tempo_a_peridodo_final.append(ultima_linha)
    nome_time_A = [sigla_time_a for item03 in range(len(tempo_a_peridodo_final))]
    posse_de_bola_a = pd.DataFrame()
    posse_de_bola_a['Time'] = nome_time_A
    posse_de_bola_a['Tempo_de_Inicio'] = tempo_b_peridodo_final
    posse_de_bola_a['Tempo_de_Termino'] = tempo_a_peridodo_final
    ########################################################################
    del (tempo_b_peridodo_final[0])
    tempo_b_peridodo_final.append(ultima_linha)
    nome_time_B = [sigla_time_b for item03 in range(len(tempo_b_peridodo_final))]
    posse_de_bola_b = pd.DataFrame()
    posse_de_bola_b['Time'] = nome_time_B
    posse_de_bola_b['Tempo_de_Inicio'] = tempo_a_peridodo_final
    posse_de_bola_b['Tempo_de_Termino'] = tempo_b_peridodo_final

# e acrescenta no a e agora tb acrescenta no B
elif len(tempo_a_peridodo_final) > len(tempo_b_peridodo_final):
    tempo_b_peridodo_final.append(ultima_linha)
    nome_time_B = [sigla_time_b for item03 in range(len(tempo_b_peridodo_final))]
    posse_de_bola_b = pd.DataFrame()
    posse_de_bola_b['Time'] = nome_time_B
    posse_de_bola_b['Tempo_de_Inicio'] = tempo_a_peridodo_final
    posse_de_bola_b['Tempo_de_Termino'] = tempo_b_peridodo_final
    ###############################################################
    del (tempo_a_peridodo_final[0])
    tempo_a_peridodo_final.append(ultima_linha)
    nome_time_A = [sigla_time_a for item03 in range(len(tempo_a_peridodo_final))]
    posse_de_bola_a = pd.DataFrame()
    posse_de_bola_a['Time'] = nome_time_A
    posse_de_bola_a['Tempo_de_Inicio'] = tempo_b_peridodo_final
    posse_de_bola_a['Tempo_de_Termino'] = tempo_a_peridodo_final

elif len(tempo_a_peridodo_final) == len(tempo_b_peridodo_final):
    if tempo_a_peridodo_final[0] == 0:
        nome_time_B = [sigla_time_b for item03 in range(len(tempo_b_peridodo_final))]
        posse_de_bola_b = pd.DataFrame()
        posse_de_bola_b['Time'] = nome_time_B
        posse_de_bola_b['Tempo_de_Inicio'] = tempo_a_peridodo_final
        posse_de_bola_b['Tempo_de_Termino'] = tempo_b_peridodo_final
        #######################################
        del (tempo_a_peridodo_final[0])
        tempo_a_peridodo_final.append(ultima_linha)
        nome_time_A = [sigla_time_a for item03 in range(len(tempo_a_peridodo_final))]
        posse_de_bola_a = pd.DataFrame()
        posse_de_bola_a['Time'] = nome_time_A
        posse_de_bola_a['Tempo_de_Inicio'] = tempo_b_peridodo_final
        posse_de_bola_a['Tempo_de_Termino'] = tempo_a_peridodo_final

    elif tempo_b_peridodo_final[0] == 0:
        nome_time_A = [sigla_time_a for item03 in range(len(tempo_a_peridodo_final))]
        posse_de_bola_a = pd.DataFrame()
        posse_de_bola_a['Time'] = nome_time_A
        posse_de_bola_a['Tempo_de_Inicio'] = tempo_b_peridodo_final
        posse_de_bola_a['Tempo_de_Termino'] = tempo_a_peridodo_final
        #######################################
        del (tempo_b_peridodo_final[0])
        tempo_b_peridodo_final.append(ultima_linha)
        nome_time_B = [sigla_time_b for item03 in range(len(tempo_b_peridodo_final))]
        posse_de_bola_b = pd.DataFrame()
        posse_de_bola_b['Time'] = nome_time_B
        posse_de_bola_b['Tempo_de_Inicio'] = tempo_a_peridodo_final
        posse_de_bola_b['Tempo_de_Termino'] = tempo_b_peridodo_final

posse_de_bola = pd.concat([posse_de_bola_a, posse_de_bola_b], ignore_index=True)
posse_de_bola.sort_values(by='Tempo_de_Inicio', ignore_index=True, inplace=True)
posse_de_bola['Tempo_de_Termino'] = posse_de_bola['Tempo_de_Termino'].astype(int)
posse_de_bola['Tempo_Posse'] = posse_de_bola['Tempo_de_Termino'] - posse_de_bola['Tempo_de_Inicio']
posse_de_bola['Tempo_Posse'] = posse_de_bola['Tempo_Posse'].apply(lambda x: abs(x))
posse_de_bola.reset_index(inplace=True, drop=True)

posse_de_bola.to_csv('tempo2.csv')

teste = posse_de_bola[posse_de_bola['Time'] == sigla_time_a]
teste.reset_index(inplace=True, drop=True)
teste1 = posse_de_bola[posse_de_bola['Time'] == sigla_time_b]
teste1.reset_index(inplace=True, drop=True)

grafico_posse_time1 = teste
grafico_posse_time1.reset_index(inplace=True)
grafico_posse_time2 = teste1
grafico_posse_time2.reset_index(inplace=True)

##########################################################
# Análise dos períodos positivos e negativos do times
# Criar um novo dataFrame para analisar os períodos positivos dos times
data = pd.DataFrame()
data['Time'] = pontuacao['Time']
data['Indicador'] = pontuacao['Indicador']
data['diff_pontuacao'] = pontuacao['diferenca_placar_visitante']
data['Tempo'] = pontuacao['Tempo']

# Utilizando a diferença do placar entre casa e visitante, aplicando diff (diferença entre as linhas)
# e usando seu valor absoluto (abs())
# nós podemos encontrar o valor de cada indicador técnico
data["pontuacao"] = data["diff_pontuacao"].diff()
data["pontuacao"] = data["pontuacao"].apply(lambda x: abs(x))

# como o primeiro valor some quando fazemos a diff e esse primeiro valor é
# importante pq é o primeiro ponto, nós adicionamos ele
novo_valor = data["diff_pontuacao"][0]
data.loc[0, 'pontuacao'] = abs(novo_valor)
data.reset_index(drop=True, inplace=True)

data['pontuacao'] = data['pontuacao'].astype(int)
data.to_csv('tempo2.csv')

# esse df é usado para retirar alguns argumentos que não fazem diferença
# na função abaixo retiramos as listas vazias que o loop gera quando o time se repete
def remove_item(my_list,*args):
    deletar = list(args)
    for item in deletar:
        while item in my_list:
            my_list.remove(item)
    return my_list

# Utilizamos uma Flag para diferenciar as paradas entre os tempos iniciais de cada posse
flag = -1
# valores da ultima linha
ultima_linha = []
# valores finais da posse de bola
tempo_a_peridodo_final = []
tempo_b_peridodo_final = []
# identifica o tempo final
tempo_a_fim = 0
tempo_b_fim = 0
# utilizado para agrupar os valores da pontuação dos times
time_a = []
time_b = []
# utilizados para somar os valores agrupados da pontuação
soma_a = []
soma_b = []

for i in range(len(data)):
    # caso corresponda ao nome do time A
    if data['Time'][i] == sigla_time_a:
        # adiciona o valor da pontuação
        time_a.append(data['pontuacao'][i])
        ##########################################
        # pegam os valores acumulados do time B e as soma
        soma_b.append(sum(time_b))
        # zera esse valor da pontuação para não interferir na mudaça do for
        time_b = []
        # remove esses valores zerados
        soma_b = remove_item(soma_b, 0)
        if flag != 1:
            # quando chegamos na flag o pensamento é pegar o primeiro valor que apresenta no Time A
            # o loop do Time B é terminado
            tempo_b_peridodo_final.append(tempo_b_fim)
            # pega o primeiro valor do tempo de início
            tempo_a_fim = data['Tempo'][i]
            flag = 1
        else:
            tempo_a_fim = data['Tempo'][i]
            flag = 1
    # caso corresponda ao nome do time B
    elif data['Time'][i] == sigla_time_b:
        # adiciona o valor da pontuação
        time_b.append(data['pontuacao'][i])
        #####################################################
        # pegam os valores acumulados do time A e as soma
        soma_a.append(sum(time_a))
        # zera esse valor da pontuação para não interferir na mudaça do for
        time_a = []
        # remove esses valores zerados
        soma_a = remove_item(soma_a, 0)
        if flag != 0:
            # quando chegamos na flag o pensamento é pegar o primeiro valor que apresenta no Time B
            # o loop do Time A é terminado
            tempo_a_peridodo_final.append(tempo_a_fim)
            # pega o primeiro valor do tempo final
            tempo_b_fim = data['Tempo'][i]
            flag = 0
        else:
            tempo_b_fim = data['Tempo'][i]
            flag = 0
    # caso corresponda ao termino da partida
    else:
        # caso chegue no final da linha os valores são armazenados
        ultima_linha = data['Tempo'][i]
        if flag != 1:
            tempo_b_peridodo_final.append(tempo_b_fim)
            # aplicamos as ultimas somas  para cada time
            # e removemos os valores que estão zerados
            soma_b.append(sum(time_b))
            soma_b = remove_item(soma_b, 0)
            soma_a.append(np.nan)
        else:
            tempo_a_peridodo_final.append(tempo_a_fim)
            # aplicamos as ultimas somas  para cada time
            # e removemos os valores que estão zerados
            soma_a.append(sum(time_a))
            soma_a = remove_item(soma_a, 0)
            soma_b.append(np.nan)

# caso o tamanho do inicio esteja variando  por causa dos ultimos lances relacionados ao tempo de partida
# a gente alinha dessa forma
if len(tempo_a_peridodo_final) < len(tempo_b_peridodo_final):
    # o fim do tempo b é o início do tempo A, pq a troca de bola é alternada
    tempo_a_peridodo_final.append(ultima_linha)
    nome_time_A = [sigla_time_a for item03 in range(len(tempo_a_peridodo_final))]
    posse_de_bola_A = pd.DataFrame()
    posse_de_bola_A['Time'] = nome_time_A
    posse_de_bola_A['Tempo_de_Inicio'] = tempo_b_peridodo_final
    posse_de_bola_A['Tempo_de_Termino'] = tempo_a_peridodo_final
    posse_de_bola_A['Soma_Pontuacao'] = soma_a
    ########################################################################
    del(tempo_b_peridodo_final[0])
    tempo_b_peridodo_final.append(ultima_linha)
    soma_b.append(np.nan)
    nome_time_B = [sigla_time_b for item03 in range(len(tempo_b_peridodo_final))]
    posse_de_bola_B = pd.DataFrame()
    posse_de_bola_B['Time'] = nome_time_B
    posse_de_bola_B['Tempo_de_Inicio'] = tempo_a_peridodo_final
    posse_de_bola_B['Tempo_de_Termino'] = tempo_b_peridodo_final
    posse_de_bola_B['Soma_Pontuacao'] = soma_b

# e acrescenta no a e agora tb acrescenta no B
if len(tempo_a_peridodo_final) > len(tempo_b_peridodo_final):
    tempo_b_peridodo_final.append(ultima_linha)
    nome_time_B = [sigla_time_b for item03 in range(len(tempo_b_peridodo_final))]
    posse_de_bola_B = pd.DataFrame()
    posse_de_bola_B['Time'] = nome_time_B
    posse_de_bola_B['Tempo_de_Inicio'] = tempo_a_peridodo_final
    posse_de_bola_B['Tempo_de_Termino'] = tempo_b_peridodo_final
    posse_de_bola_B['Soma_Pontuacao'] = soma_b
    ###############################################################
    del(tempo_a_peridodo_final[0])
    tempo_a_peridodo_final.append(ultima_linha)
    soma_a.append(np.nan)
    nome_time_A = [sigla_time_a for item03 in range(len(tempo_a_peridodo_final))]
    posse_de_bola_A = pd.DataFrame()
    posse_de_bola_A['Time'] = nome_time_A
    posse_de_bola_A['Tempo_de_Inicio'] = tempo_b_peridodo_final
    posse_de_bola_A['Tempo_de_Termino'] = tempo_a_peridodo_final
    posse_de_bola_A['Soma_Pontuacao'] = soma_a

if len(tempo_a_peridodo_final) == len(tempo_b_peridodo_final):
    if tempo_a_peridodo_final[0] == 0:
        nome_time_B = [sigla_time_b for item03 in range(len(tempo_b_peridodo_final))]
        posse_de_bola_B = pd.DataFrame()
        posse_de_bola_B['Time'] = nome_time_B
        posse_de_bola_B['Tempo_de_Inicio'] = tempo_a_peridodo_final
        posse_de_bola_B['Tempo_de_Termino'] = tempo_b_peridodo_final
        posse_de_bola_B['Soma_Pontuacao'] = soma_b
        #######################################
        del(tempo_a_peridodo_final[0])
        tempo_a_peridodo_final.append(ultima_linha)
        nome_time_A = [sigla_time_a for item03 in range(len(tempo_a_peridodo_final))]
        posse_de_bola_A = pd.DataFrame()
        posse_de_bola_A['Time'] = nome_time_A
        posse_de_bola_A['Tempo_de_Inicio'] = tempo_b_peridodo_final
        posse_de_bola_A['Tempo_de_Termino'] = tempo_a_peridodo_final
        posse_de_bola_A['Soma_Pontuacao'] = soma_a
    elif tempo_b_peridodo_final[0] == 0:
        nome_time_A = [sigla_time_a for item03 in range(len(tempo_a_peridodo_final))]
        posse_de_bola_A = pd.DataFrame()
        posse_de_bola_A['Time'] = nome_time_A
        posse_de_bola_A['Tempo_de_Inicio'] = tempo_b_peridodo_final
        posse_de_bola_A['Tempo_de_Termino'] = tempo_a_peridodo_final
        posse_de_bola_A['Soma_Pontuacao'] = soma_a
        #######################################
        del(tempo_b_peridodo_final[0])
        tempo_b_peridodo_final.append(ultima_linha)
        nome_time_B = [sigla_time_b for item03 in range(len(tempo_b_peridodo_final))]
        posse_de_bola_B = pd.DataFrame()
        posse_de_bola_B['Time'] = nome_time_B
        posse_de_bola_B['Tempo_de_Inicio'] = tempo_a_peridodo_final
        posse_de_bola_B['Tempo_de_Termino'] = tempo_b_peridodo_final
        posse_de_bola_B['Soma_Pontuacao'] = soma_b

posse_de_bola_bruta = pd.concat([posse_de_bola_A, posse_de_bola_B], ignore_index=True)
posse_de_bola_bruta.sort_values(by='Tempo_de_Inicio', ignore_index=True, inplace=True)
posse_de_bola_bruta["diff_pontuacao"] = posse_de_bola_bruta["Soma_Pontuacao"].diff()

periodos_posteriores = []
for i in range(len(posse_de_bola_bruta)):
    if posse_de_bola_bruta['Soma_Pontuacao'][i] >= 5:
        periodo_potencial_a_positivo = 1
    else:
        if (posse_de_bola_bruta['diff_pontuacao'][i] <= -4) & (posse_de_bola_bruta['Soma_Pontuacao'][i] < 3):
            periodos_posteriores.append(posse_de_bola_bruta['Tempo_de_Inicio'][i])
            if periodo_potencial_a_positivo == 1:
                periodo_potencial_a_positivo = 0
            elif periodo_potencial_a_positivo != 1:
                periodo_potencial_a_positivo = 0


periodos_iniciais = posse_de_bola_bruta[~posse_de_bola_bruta['Tempo_de_Inicio'].isin(periodos_posteriores)]
periodos_iniciais.reset_index(inplace=True, drop=True)

flag = -1
tempo_a_peridodo_inicial = []
tempo_b_peridodo_inicial = []
tempo_a_peridodo_final = []
tempo_b_peridodo_final = []
pontuação_a = []
pontuação_b = []
nome_time_A = []
nome_time_B = []
# como o time do flamengo começa, o time de minas não apresenta o primeiro valor
# por causa disso é acrescentado um valor 0 que não existe
potencial_final_periodo_a = 0
potencial_final_periodo_b = 0

for i in range(len(periodos_iniciais)):
    if periodos_iniciais['Time'][i] == sigla_time_a:
        if flag != 1:
            potencial_final_periodo_a = periodos_iniciais['Tempo_de_Termino'][i]
            tempo_a_peridodo_inicial.append(periodos_iniciais['Tempo_de_Inicio'][i])
            nome_time_A.append(periodos_iniciais['Time'][i])
            pontuação_a.append(periodos_iniciais['Soma_Pontuacao'][i])
            ##################################################################
            tempo_b_peridodo_final.append(potencial_final_periodo_b)
            flag = 1
        else:
            potencial_final_periodo_a = periodos_iniciais['Tempo_de_Termino'][i]
            flag = 1
    else:
        if flag != 0:
            tempo_a_peridodo_final.append(potencial_final_periodo_a)
            ############################################################
            potencial_final_periodo_b = periodos_iniciais['Tempo_de_Termino'][i]
            tempo_b_peridodo_inicial.append(periodos_iniciais['Tempo_de_Inicio'][i])
            nome_time_B.append(periodos_iniciais['Time'][i])
            pontuação_b.append(periodos_iniciais['Soma_Pontuacao'][i])
            flag = 0
        else:
            potencial_final_periodo_b = periodos_iniciais['Tempo_de_Termino'][i]
            flag = 0

if len(tempo_a_peridodo_final) == len(tempo_b_peridodo_final):
    if tempo_a_peridodo_final[0] == 0:
        periodos_B = pd.DataFrame()
        periodos_B['Time'] = nome_time_B
        periodos_B['Tempo_de_Inicio'] = tempo_b_peridodo_inicial
        periodos_B['Tempo_de_Termino'] = tempo_b_peridodo_final
        periodos_B['Soma_Pontuacao'] = pontuação_b
        #######################################
        del(tempo_a_peridodo_final[0])
        tempo_a_peridodo_final.append(ultima_linha)
        periodos_A = pd.DataFrame()
        periodos_A['Time'] = nome_time_A
        periodos_A['Tempo_de_Inicio'] = tempo_a_peridodo_inicial
        periodos_A['Tempo_de_Termino'] = tempo_a_peridodo_final
        periodos_A['Soma_Pontuacao'] = pontuação_a
    elif tempo_b_peridodo_final[0] == 0:
        periodos_A = pd.DataFrame()
        periodos_A['Time'] = nome_time_A
        periodos_A['Tempo_de_Inicio'] = tempo_a_peridodo_inicial
        periodos_A['Tempo_de_Termino'] = tempo_a_peridodo_final
        periodos_A['Soma_Pontuacao'] = pontuação_a
        #######################################
        del(tempo_b_peridodo_final[0])
        tempo_b_peridodo_final.append(ultima_linha)
        periodos_B = pd.DataFrame()
        periodos_B['Time'] = nome_time_B
        periodos_B['Tempo_de_Inicio'] = tempo_b_peridodo_inicial
        periodos_B['Tempo_de_Termino'] = tempo_b_peridodo_final
        periodos_B['Soma_Pontuacao'] = pontuação_b

periodo = pd.concat([periodos_A, periodos_B], ignore_index=True)
periodo.sort_values(by='Tempo_de_Inicio', ignore_index=True, inplace=True)
periodo_final_a = periodo.loc[(periodo['Soma_Pontuacao'] >= 5) & (periodo['Time'] == sigla_time_a)]

periodo_final_a_inicio = list(periodo_final_a['Tempo_de_Inicio'])
periodo_final_a_final = list(periodo_final_a['Tempo_de_Termino'])

periodo_final_b = periodo.loc[(periodo['Soma_Pontuacao'] >= 5) & (periodo['Time'] == sigla_time_b)]
periodo_final_b_inicio = list(periodo_final_b['Tempo_de_Inicio'])
periodo_final_b_final = list(periodo_final_b['Tempo_de_Termino'])

