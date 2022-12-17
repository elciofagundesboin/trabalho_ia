# importing the required module
import matplotlib.pyplot as plt
import numpy as np

# calcula a media dos valores de um conjunto de arquivos
def calcula_media(musicas):
    file = open('resultado/Media.txt', 'a+', encoding='utf-8')

    # le os arquivos de entrada e salva o resultado de cada um em um vetor
    vetor_resultados = []
    for i in range(len(musicas)):
        vetor_resultados.append(le_arquivo(musicas))
    
    for l in range(len(musicas)):
        x = []
    for i in range (5):
        for j in range(5):
            valores = []
            for k in range(len(musicas)):
                valores.append(vetor_resultados[i][j])
            
            soma = sum(valores)
            media = soma / len(valores)
            print('Media= '+ str(media))
            #file.write(str(media) + '\n')

    file.close()

# lê um arquivo de resultados e retorna um array de arrays com os valores
def le_arquivo(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    modelo = []
    k = 0
    for i in range(5):
        kbps = []
        for j in range(5):
            kbps.append(lines[k])
            k += 1
        modelo.append(kbps)
            
    print(modelo[0])
    #return modelo

# função que ajusta os valores para percentual com duas casas decimais
def formata_percentual(valores):
    for i in range(len(valores)):
        current_element = valores[i]
        valores[i] = (round(current_element * 100, 2))
    return valores

# função que gera o gráfico
def constroi_grafico(arquivo):

    labels = ['Tiny', 'Base', 'Small', 'Medium', 'Large']
    kbps64 = formata_percentual(le_arquivo(arquivo, '64'))
    kbps128 = formata_percentual(le_arquivo(arquivo, '128'))
    kbps192 = formata_percentual(le_arquivo(arquivo, '192'))
    kbps256 = formata_percentual(le_arquivo(arquivo, '256'))
    kbps320 = formata_percentual(le_arquivo(arquivo, '320'))

    x = np.arange(len(labels))  # localização dos títulos
    width = 0.16  # largura das barras

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width*2, kbps64, width, label='64 kbps')
    rects2 = ax.bar(x - width, kbps128, width, label='128 kbps')
    rects3 = ax.bar(x, kbps192, width, label='192 kbps')
    rects4 = ax.bar(x + width, kbps256, width, label='256 kbps')
    rects5 = ax.bar(x + width*2, kbps320, width, label='320 kbps')

    ax.set_ylabel('Percentual de Erro (%)')
    ax.set_title('Percentual de Erro (WER com bitrates diferentes')
    ax.set_xticks(x, labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    ax.bar_label(rects3, padding=3)
    ax.bar_label(rects4, padding=3)
    ax.bar_label(rects5, padding=3)

    fig.tight_layout()

    plt.show()

# EXECUTA AS FUNCIONALIDADES
#constroi_grafico('Faroeste Caboclo')
#constroi_grafico('Cuando Suba La Marea')

#musicas = ['Faroeste Caboclo', 'Cuando Suba La Marea']
#calcula_media(musicas)
#constroi_grafico('Media')

le_arquivo('resultado/tempos/Wellerman.txt')