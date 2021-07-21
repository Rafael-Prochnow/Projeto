








'''plt.style.use('seaborn')
        sns.set_style('white')
        plt.figure(figsize=(9, 5))
        tempo = pontuacao['Tempo']
        pontuacao1 = pontuacao['placar_casa']
        pontuacao2 = pontuacao['placar_visitante']
        plt.plot(tempo, pontuacao1, label='placar_casa')
        plt.plot(tempo, pontuacao2, label='placar_visitante')
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1), prop={'size': 14})
        for x in quartos:
            plt.axvline(x, color='red', label=pontuacao.index, linestyle='--', alpha=0.4)
        plt.title('Gráfico do Placar Acumulativo do Jogo', fontsize=18)
        plt.ylabel('Pontos')
        plt.xlabel('Segundos')
        plt.tight_layout()
        plt.show()'''


'''plt.style.use('seaborn')
        sns.set_style('white')
        plt.figure(figsize=(11, 5))
        sns.barplot(x='index', y='Time_Novo', data=grafico_posse_time1, color='black')
        plt.title(f'Ataques do {nome_time_casa} no jogo', fontsize=20)
        plt.yticks([5, 10, 14, 24], fontsize=16)
        plt.ylabel('Tempo', fontsize=16)
        plt.xlabel('Ataques', fontsize=16)
        plt.xticks(x[::frequency], my_xticks[::frequency], fontsize=14)
        valores = [24, 14, 10, 5]
        for i in valores:
            plt.axhline(i, color='red', alpha=0.6, label=f'{i} segundos')
        # plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1), prop={'size':14})
        plt.show()'''

'''plt.style.use('seaborn')
        sns.set_style('white')
        plt.figure(figsize=(11, 5))
        sns.barplot(x='index', y='Time_Novo', data=grafico_posse_time2, color='black')
        plt.title(f'Ataques do {nome_time_fora} no jogo', fontsize=20)
        plt.yticks([5, 10, 14, 24], fontsize=16)
        plt.ylabel('Tempo', fontsize=16)
        plt.xlabel('Ataques', fontsize=16)
        plt.xticks(x2[::frequency2], my_xticks2[::frequency2], fontsize=14)
        valores = [24, 14, 10, 5]
        for i in valores:
            plt.axhline(i, color='red', alpha=0.6, label=f'{i} segundos')
        # plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1), prop={'size':14})
        plt.show()'''

'''#  Gráfico da diferença da placar
        plt.style.use('seaborn')
        sns.set_style('white')
        plt.figure(figsize=(11, 5))
        plt.plot(posse_de_bola['Tempo_Fim'], posse_de_bola['dif_casa'], color='black')
        plt.title('Diferença do Placar Casa Durante a Partida', fontsize=10)
        plt.ylabel('Diferença do Placar', fontsize=10)
        plt.xlabel('Tempo de Jogo em Segundos', fontsize=10)
        plt.yticks(fontsize=10)
        plt.xticks(fontsize=10)
        # plt.legend(loc='upper left', bbox_to_anchor=(1, 1), prop={'size':14})
        for x in quartos:
            plt.axvline(x, color='red', label=posse_de_bola.index, linestyle='--', alpha=0.4)
        plt.axhline(0, color='orange', label=posse_de_bola.index, alpha=0.5)
        plt.show()'''


'''
        if len(segmento) <= 2:
            # GRÁFICO
            plt.style.use('seaborn')
            sns.set_style('white')
            plt.figure(figsize=(11, 5))
            plt.plot(posse_de_bola['Tempo_Fim'], posse_de_bola['dif_casa'], color='black')
            plt.title('Diferença do Placar Casa Durante a Partida', fontsize=12)
            plt.ylabel('Diferença do Placar', fontsize=10)
            plt.xlabel('Tempo de Jogo em Segundos', fontsize=10)
            plt.yticks(fontsize=10)
            plt.xticks(fontsize=10)
            final_t = []
            final_dif = []
            for i in segmento:
                selecao = (posse_de_bola['Tempo_Fim'] >= i[0]) & (posse_de_bola['Tempo_Fim'] <= i[1])
                df_filtado_dif = posse_de_bola[selecao]['dif_casa']
                df_filtado_t = posse_de_bola[selecao]['Tempo_Fim']
                plt.plot(df_filtado_t, df_filtado_dif, color='red')
            for x in quartos:
                plt.axvline(x, color='red', label=posse_de_bola.index, linestyle='--', alpha=0.4)
            plt.axhline(0, color='orange', label=posse_de_bola.index, alpha=0.5)
            plt.show()'''

'''
        if len(segmento_dois) <= 2:
            # GRÁFICO
            plt.style.use('seaborn')
            sns.set_style('white')
            plt.figure(figsize=(11, 5))
            plt.plot(posse_de_bola['Tempo_Fim'], posse_de_bola['dif_casa'], color='black')
            plt.title('Diferença do Placar Casa Durante a Partida', fontsize=12)
            plt.ylabel('Diferença do Placar', fontsize=10)
            plt.xlabel('Tempo de Jogo em Segundos', fontsize=10)
            plt.yticks(fontsize=10)
            plt.xticks(fontsize=10)
            final_t = []
            final_dif = []
            for i in segmento_dois:
                selecao_dois = (posse_de_bola['Tempo_Fim'] >= i[0]) & (posse_de_bola['Tempo_Fim'] <= i[1])
                df_filtado_dif = posse_de_bola[selecao_dois]['dif_casa']
                df_filtado_t = posse_de_bola[selecao_dois]['Tempo_Fim']
                plt.plot(df_filtado_t, df_filtado_dif, label='diferença do placar', color='red')
            for x in quartos:
                plt.axvline(x, color='red', label=posse_de_bola.index, linestyle='--', alpha=0.4)
            plt.axhline(0, color='orange', label=posse_de_bola.index, alpha=0.5)
            plt.show()'''