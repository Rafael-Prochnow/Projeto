import pandas as pd

'''
algumas coisas para fazer antes de poder fazer as análises é
    -> melhorar o replace usando algum def ou list conprehetion ()
    -> definir qual coluna é floot ou int ()
    -> melhorar os funções realizadas com lambda e for ()
___________________________________________________________________________________________________    
    -> precisa definir 3 casas decimais depois da vírgula
    -> redefinir a primeira coluna que apresenta o número de jogadores no time 'Njogador' ()
    -> precisa tirar da linha 335 a substituição do : para . pois é a hora (ok)
            (perguntar pois tem tabelas que o horário é diferente)
    -> precisa acrescentar mais uma coluna indicando "classificatória/Playoffs" ()
    -> precisa de uma coluna "vitório/derrota" ()
    -> precis colocar outra coluna para "difereça no placar" 
    -> precisa colocar o dia e horário do jogo na tabela principal 
            -> colocar 200 min para EQUIPE (40"x 5 jogadores) | somar todos os min dos jogadores
            -> localizar os jogos que apresentam Overtime
            -> df_full['Min'] = df_full['Min'].str.replace(':', '.')
    -> precisa colocar colunas que representam a Frequencia Relativa dos indicadores de 
    cada jogador a partir do seu time         
    -> numero médio de jogadores que jogaram 
    -> modificar a coluna Casa/Fora em valores casa/fora e não mais 0/1
    -> renomear as colunas para:
    "Njogador", "Temporada", "Time", "Adv", "C_F", "Jogador", "Min", "Pts_C", "Pts_T", "AR_3_C",
    "AR_3_T", "AR_2_C", "AR_2_T", "LL_C", "LL_T", "RO", "RD", "RT", "AS", "BR", "TO", "FC",
    "FR", "ER", "EN"
    -> analise['Pace'] pace análisar por jogador
    -> precisa da posição do cara
____________________________________________________________________________________________________    
    -> Há jogador com nomes diferentes!!!!!!!!!!!! na mão isso     
        
____________________________________________________________________________________________________    
    -> questão da probabilidade das coisas acontecerem para depois serem avaliadas as tomadas de
    decisão dos treinadores deve ser dado pelo mapa mental estabelecido por nós 
    -> analisar as tomadas de decisão dos treinadores envolve muitos fatores como: quando 
    o jogador precisa ganhar ritmo no time; jogador novo precisa ganhar experiência ....
'''

dados = pd.read_csv("Tabela_geral_2019.csv")

# precisa tirar essa coluna que não serva para nada
dados.columns = ["Njogador", "Temporada", "Time", "Adv", "C_F", "Jogador", "Min", "Pts_C", "Pts_T", "Pts_3_C",
                 "Pts_3_T", "Pts_2_C", "Pts_2_T", "LL_Pts_C", "LL_Pts_T", "RO", "RD", "RT", "AS", "BR", "TO", "FC",
                 "FR", "ER", "EN"]

# precisa colocar tirar a marcação (T) pois atapalha os nomes e não tem em todas as tabelas
nome_com_T = dados['Jogador'].str.translate({ord(c): "," for c in "()"})
nome_sem_T = nome_com_T.str.replace(' ,T,', '')
dados['Jogador'] = nome_sem_T

# substituir os nomes de Equipes e Total. Deixar padrão.
dados['Jogador'] = dados['Jogador'].str.replace('Total', 'Equipe')

# substitui os valores nulos por 0
dados.fillna(0, inplace=True)
# para verificar só aplicar linha abaixo
# enulo = dados.isnull().sum()
# converter os dados de float para int

dados['Pts_C'] = dados.Pts_C.astype(int)
dados['Pts_T'] = dados.Pts_T.astype(int)
dados['Pts_3_C'] = dados.Pts_3_C.astype(int)
dados['Pts_3_T'] = dados.Pts_3_T.astype(int)
dados['Pts_2_C'] = dados.Pts_2_C.astype(int)
dados['Pts_2_T'] = dados.Pts_2_T.astype(int)
dados['LL_Pts_C'] = dados.LL_Pts_C.astype(int)
dados['LL_Pts_T'] = dados.LL_Pts_T.astype(int)
dados['AS'] = dados.AS.astype(int)
dados['BR'] = dados.BR.astype(int)
dados['TO'] = dados.TO.astype(int)
dados['FC'] = dados.FC.astype(int)
dados['FR'] = dados.FR.astype(int)
dados['ER'] = dados.ER.astype(int)
dados['EN'] = dados.EN.astype(int)

# deixando os minutos normais (deixado com :)
dados['Min'] = dados.Min.astype(str)
dados['Min'] = dados['Min'].str.replace('.', ':')

dados.to_csv("Tabela_geral_2019_nova.csv")
'''
print(dados.shape)  # mostra o número de linhas e colunas

print(dados.columns)

# usar .query(temporada==19) faz com que ele localize as variáveis que vc quer
# qual que é a descrição das informações que temos dos dados presentes?
# como a variável é uma str precisa colocar entre ''
inf_jogos = dados.query("Jogador=='Total' or Jogador=='Equipe'")
print(inf_jogos.describe())

# para não correr o risco de não juntar um dataframe com uma série ou outra dataframe que não estarem 
# em quantidades diferentes utilizamos o .join

# podemos agrupar os valores que queremos analisar, como cada jogador ou time usando groupby()
avaliacoes_jogadores = dados.groupby("Jogador").mean()
# colocando em ordem do menor para o maior usando o sort_values (cescente)
# colocando em ordem do maior para o menor usando sort_values com o ansceding=False (decescente)
atleta_Georginho = dados.query("Jogador=='Georginho'").reset_index(drop=True)

# print(atleta_Georginho)
print(atleta_Georginho["Pts_C"].values)

plt.plot(atleta_Georginho["Pts_C"].values)
plt.show()

'''
