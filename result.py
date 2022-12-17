# importing the required module
import matplotlib.pyplot as plt
import numpy as np

# lê um arquivo de resultados e retorna um array de arrays com os valores
def le_arquivo(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    modelo = []
    k = 0
    for i in range(5):
        kbps = []
        for j in range(5):
            kbps.append(float(lines[k]))
            k += 1
        modelo.append(kbps)
            
    #print(modelo)
    return modelo

# calcula a media dos valores de um conjunto de arquivos
def calcula_media(musicas, arquivo_saida):
    file = open(arquivo_saida, 'a+', encoding='utf-8')

    # le os arquivos de entrada e salva o resultado de cada um em um vetor
    vetor_resultados = []
    for i in range(len(musicas)):
        vetor_resultados.append(le_arquivo(musicas[i]))
    
    for i in range (5):
        for j in range(5):
            valores = []
            for resultado in vetor_resultados:
                valores.append(resultado[i][j])
            
            soma = sum(valores)
            media = soma / len(valores)
            print('Media= '+ str(media))
            file.write(str(media) + '\n')

    file.close()

# função que ajusta os valores para percentual com duas casas decimais
def formata_percentual(valores):
    for i in range(len(valores)):
        current_element = valores[i]
        valores[i] = (round(current_element * 100, 2))
    return valores

# função que ajusta os valores para percentual com duas casas decimais
def formata_tempo(valores):
    for i in range(len(valores)):
        current_element = valores[i]
        valores[i] = (round(current_element, 2))
    return valores


# função que gera o gráfico
def constroi_grafico(arquivo_wer, arquivo_tempos):

    labels = ['Tiny', 'Base', 'Small', 'Medium', 'Large']
    
    x = np.arange(len(labels))  # localização dos títulos
    x = x
    width = 0.18  # largura das barras
    
    #--------------------------------------------------------------------
    result64 = le_arquivo(arquivo_wer)
    result128 = le_arquivo(arquivo_wer)
    result192 = le_arquivo(arquivo_wer)
    result256 = le_arquivo(arquivo_wer)
    result320 = le_arquivo(arquivo_wer)
    
    wer_kbps64 = formata_percentual(result64[0])
    wer_kbps128 = formata_percentual(result128[1])
    wer_kbps192 = formata_percentual(result192[2])
    wer_kbps256 = formata_percentual(result256[3])
    wer_kbps320 = formata_percentual(result320[4])
    
    fig, ax  = plt.subplots(figsize=(15, 4))
    ax = plt.subplot()
    rects1 = ax.bar(x - width*2, wer_kbps64, width, label='64 kbps')
    rects2 = ax.bar(x - width, wer_kbps128, width, label='128 kbps')
    rects3 = ax.bar(x, wer_kbps192, width, label='192 kbps')
    rects4 = ax.bar(x + width, wer_kbps256, width, label='256 kbps')
    rects5 = ax.bar(x + width*2, wer_kbps320, width, label='320 kbps')

    ax.set_ylabel('Percentual de Erro (%)')
    ax.set_title('Percentual de Erro (WER com bitrates diferentes)')
    ax.set_xticks(x, labels)
    ax.legend()
    
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    ax.bar_label(rects3, padding=3)
    ax.bar_label(rects4, padding=3)
    ax.bar_label(rects5, padding=3)

    fig.tight_layout()
    #--------------------------------------------------------------------
    result64 = le_arquivo(arquivo_tempos)
    result128 = le_arquivo(arquivo_tempos)
    result192 = le_arquivo(arquivo_tempos)
    result256 = le_arquivo(arquivo_tempos)
    result320 = le_arquivo(arquivo_tempos)
    
    tempo_kbps64 = formata_tempo(result64[0])
    tempo_kbps128 = formata_tempo(result128[1])
    tempo_kbps192 = formata_tempo(result192[2])
    tempo_kbps256 = formata_tempo(result256[3])
    tempo_kbps320 = formata_tempo(result320[4])
    
    fig, ax  = plt.subplots(figsize=(15, 4))
    ax = plt.subplot()
    rects1 = ax.bar(x - width*2, tempo_kbps64, width, label='64 kbps')
    rects2 = ax.bar(x - width, tempo_kbps128, width, label='128 kbps')
    rects3 = ax.bar(x, tempo_kbps192, width, label='192 kbps')
    rects4 = ax.bar(x + width, tempo_kbps256, width, label='256 kbps')
    rects5 = ax.bar(x + width*2, tempo_kbps320, width, label='320 kbps')

    ax.set_ylabel('Tempo de processamento (segundos)')
    ax.set_title('Tempo de processamento Wisper')
    ax.set_xticks(x, labels)
    ax.legend()
    
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    ax.bar_label(rects3, padding=3)
    ax.bar_label(rects4, padding=3)
    ax.bar_label(rects5, padding=3)

    fig.tight_layout()
    #--------------------------------------------------------------------

    plt.show()

# EXECUTA AS FUNCIONALIDADES
#wer_musicas = ['resultado/wer/The Sound of Silence.txt', 'resultado/wer/Wellerman.txt']
#calcula_media(wer_musicas, 'resultado/Media-WER.txt')
#tempos_musicas = ['resultado/tempos/The Sound of Silence.txt', 'resultado/tempos/Wellerman.txt']
#calcula_media(tempos_musicas, 'resultado/Media-Tempos.txt')
constroi_grafico('resultado/Media-WER.txt', 'resultado/Media-Tempos.txt')