'''import pandas as pd
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

'''
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.utils import shuffle
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import mean_squared_error, roc_curve, confusion_matrix, ConfusionMatrixDisplay
import pandas as pd
df = pd.read_excel('ex.xlsx')
# Classificação -1 para derrota e 1 para vitória
df['Vitoria/Derrota'].replace('vitória', 1, inplace=True)
df['Vitoria/Derrota'].replace('derrota', -1, inplace=True)
df.drop(['Unnamed: 0'], axis=1, inplace=True)
df['EF_3'] = df['Pts_3_C'] / df['Pts_3_T']
df['EF_2'] = df['Pts_2_C'] / df['Pts_2_T']
df['EF_LL'] = df['LL_C'] / df['LL_T']

# Classificação supervisionado
# Classificadores lineares
ano = 2013
a = True


# Separando os dados para cada tipo de classe
def separacao(X, D):
    X_C1 = []
    D_C1 = []
    X_C2 = []
    D_C2 = []
    for i in range(len(X)):
        if D[i] == 1:
            X_C2.append(X[i])
            D_C2.append(D[i])
        else:
            X_C1.append(X[i])
            D_C1.append(D[i])
    return np.array(X_C1), np.array(D_C1), np.array(X_C2), np.array(D_C2)


def classificador_lenear(dados, condicao_temporada, temporada, condicao_ind, indicadores):
    # Classificação -1 para derrota e 1 para vitória
    dados['Vitoria/Derrota'].replace('vitória', 1, inplace=True)
    dados['Vitoria/Derrota'].replace('derrota', -1, inplace=True)
    dados.drop(['Unnamed: 0'], axis=1, inplace=True)
    dados['EF_3'] = dados['Pts_3_C'] / dados['Pts_3_T']
    dados['EF_2'] = dados['Pts_2_C'] / dados['Pts_2_T']
    dados['EF_LL'] = dados['LL_C'] / dados['LL_T']

    dados = dados.loc[:, ['Vitoria/Derrota', 'Data', 'Casa/Fora', 'EF_3', 'EF_2', 'EF_LL', 'RO', 'RD', 'RT',
                          'AS', 'BR', 'TO', 'FC', 'ER', 'substituicao_sai', 'Periodos_Positivos', 'posse_de_bola']]
    if condicao_temporada:
        dados = dados[dados['Data'] == temporada]
        dados.reset_index(drop=True, inplace=True)
    else:
        pass

    if condicao_ind:
        # Atributos utilizados
        X = df[indicadores].to_numpy()
        D = df['Vitoria/Derrota'].to_numpy()
        # Criando as variáveis em np
        X_C1, D_C1, X_C2, D_C2 = separacao(X, D)
        # Figuras
        plt.figure(figsize=(13, 3.5))
        plt.subplot(1, 2, 1)
        plt.title('Dispersão dos Dados', fontsize=20)
        plt.xlabel('X[0]', fontsize=20)
        plt.ylabel('X[1]', fontsize=20)
        plt.scatter(X_C1[:, 0], X_C1[:, 1], marker='o', c='b')
        plt.scatter(X_C2[:, 0], X_C2[:, 1], marker='o', c='r')

        plt.subplot(1, 2, 2)
        plt.title('Histograma dos Dados', fontsize=20)
        plt.xlabel('X_C2[0]', fontsize=20)
        plt.ylabel('X_C1[0]', fontsize=20)
        plt.hist(X_C2[:, 0], color='r')
        plt.hist(X_C1[:, 0], color='b')
        plt.show()
    else:
        # Atributos utilizados
        X = df[['EF_3', 'EF_2', 'EF_LL', 'RO', 'RD', 'RT', 'AS', 'BR', 'TO', 'FC', 'ER',
                'substituicao_sai', 'Periodos_Positivos', 'posse_de_bola']].to_numpy()
        D = df['Vitoria/Derrota'].to_numpy()
        # Criando as variáveis em np
        X_C1, D_C1, X_C2, D_C2 = separacao(X, D)

    # Treinamento do classificador linear (mínimos quadrados) para o problema de classificação expresso nos dados
    prop_test = 0.30  # proporção para o teste
    x_train, x_test, d_train, d_test = train_test_split(X, D, test_size=prop_test)

    # Criar um modelo para conter todas as informações no meu modelo de Regressão Linear
    model_reg_linear = LinearRegression()
    # Ajustar o modelo
    model_reg_linear.fit(x_train, d_train)

    y_hat_train = model_reg_linear.predict(x_train)
    d_hat_tain = np.sign(y_hat_train)

    # Quero um vetor que da 1 para a posição onde tem erro e 0 na posição que não tem erro
    # Vetor de indicador de erro de treinamento
    error_train = np.abs((d_hat_tain - d_train) / 2)
    acc_train = 1 - (np.sum(error_train) / error_train.size)
    print('Acurácia de treinamento do Classificador Linear', acc_train)

    if condicao_ind:
        w_LS = np.zeros(3)
        w_LS[0] = model_reg_linear.intercept_
        w_LS[1] = model_reg_linear.coef_[0]
        w_LS[2] = model_reg_linear.coef_[1]

        xlaux = np.linspace(X.min(), X.max(), 2000)
        x2aux = -(w_LS[1] / w_LS[2]) * xlaux - (w_LS[0] / w_LS[2])

        plt.title('Dispersão dos Dados', fontsize=20)
        plt.xlabel('X[0]', fontsize=20)
        plt.ylabel('X[1]', fontsize=20)
        plt.scatter(X_C1[:, 0], X_C1[:, 1], marker='o', c='b')
        plt.scatter(X_C2[:, 0], X_C2[:, 1], marker='o', c='r')
        plt.plot(xlaux, x2aux, 'k')
        plt.show()
    else:
        pass

    # Curva ROC
    # Saida dos limiares que são utilizados para construir
    # fpr = False Positive Rating
    # tpr = True Positive Rating
    fpr_train, tpr_train, thresholds_train = roc_curve(d_train, y_hat_train)

    plt.figure()
    plt.plot(fpr_train, tpr_train)
    plt.title('Curva ROC', fontsize=20)
    plt.xlabel('False Positive', fontsize=20)
    plt.ylabel('True Positive', fontsize=20)
    plt.show()

    # Matriz de confusão
    Conf_Matriz_train = confusion_matrix(d_train, d_hat_tain)
    # Realizar o plot da matriz de confusão
    disp = ConfusionMatrixDisplay(confusion_matrix=Conf_Matriz_train)
    disp.plot()
    plt.title('Matriz de Confusão', fontsize=20)
    plt.xlabel('Predicted Label', fontsize=20)
    plt.ylabel('True Label', fontsize=20)



