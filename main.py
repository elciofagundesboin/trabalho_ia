# Importa o modelo Wisper
import whisper
# Importa a bilbioteca Jiwer
import jiwer
# Importa as bibliotecas de time
import time
import timeit
# Importa as bibliotecas para o gráfico
import matplotlib.pyplot as plt
import numpy as np

# Função para processar o Wisper
def processa_musica(musica):
    # abre o arquivo que irá gravar o WER
    print('\nInício do Processamento Wisper!\n--')
    caminho_saida = 'resultado/tempos/'+ musica +'.txt'
    f_output = open(caminho_saida, "w+", encoding='utf-8')

    modelos = ['tiny','base','small','medium','large']
    for modelo in modelos:
        kbps = 64
        for i in range (5):
            # ---
            # Carrega o modelo
            model = whisper.load_model(modelo)
            # Inicia o contador de tempo
            inicio = timeit.default_timer()
            # Processa a música
            local_musica = 'audio/'+ str(kbps) +'/'+ musica +'.mp3'
            result = model.transcribe(local_musica)
            # finaliza o contador de tempo
            fim = timeit.default_timer()
            # Abre o arquivo de saída em modo leitura
            arquivo_saida = musica +'-'+ str(kbps) +'-'+ modelo +'.txt'
            file = open('saida_wer/'+ arquivo_saida, 'w+', encoding='utf-8')
            # Escreve no arquivo o texto gerado
            file.write(result['text'])
            # Fecha o arquivo
            file.close()
            # grava o resultado no arquivo de saída
            f_output.write(str(fim - inicio) + '\n')
            print('Processado: '+ modelo +' | '+ local_musica + ' | Tempo: '+ str(fim - inicio) +' segundos')
            # ---
            kbps += 64
    
    # fecha o arquivo de saída
    f_output.close()
    print('\nProcessamento Wisper Concluído!\n--')

# Função que calcula o wer da música
def calcula_erro(musica):
    print('\nInício do Processamento WER!\n--')
    # abre o arquivo que irá gravar o WER
    caminho_saida = 'resultado/wer/'+ musica + '.txt'
    f_output = open(caminho_saida, "w+", encoding='utf-8')

    modelos = ['tiny','base','small','medium','large']
    for modelo in modelos:
        # abre o arquivo com o texto original (letra)
        caminho_origem = 'letras/'+ musica +' - Letra.txt'
        f_origem = open(caminho_origem, 'r', encoding='utf-8')
        texto_origem = f_origem.read()
        f_origem.close()
        
        kbps = 64
        for i in range (5):
            # abre o arquivo com o texto de hipotese (resultado do wisper)
            caminho_hipotese = 'saida_wer/'+ musica +'-'+ str(kbps) +'-'+ modelo + '.txt'
            f_hipotese = open(caminho_hipotese, 'r', encoding='utf-8')
            texto_hipotese = f_hipotese.read()
            f_hipotese.close()

            # calcula o WER (nesta etapa remove alguns espaços "em branco", como quebras de linha)
            measures = jiwer.compute_measures(jiwer.RemoveWhiteSpace(replace_by_space=True)(texto_origem), texto_hipotese)
            wer = measures['wer']
            # imprime na tela e grava o resultado do WER no arquivo de saída
            print('WER ('+ caminho_origem +')('+ caminho_hipotese +'): '+ str(wer))
            # grava o resultado no arquivo de saída
            f_output.write(str(wer) + '\n')
            kbps += 64
    # fecha o arquivo de saída
    f_output.close()
    print('\nProcessamento WER Concluído!\n--')

# Função que lê um arquivo de resultados e retorna um array de arrays com os valores
def le_arquivo(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    file.close()
    
    modelo = []
    k = 0
    for i in range(5):
        kbps = []
        for j in range(5):
            kbps.append(float(lines[k]))
            k += 1
        modelo.append(kbps)
    
    return modelo

# calcula a media dos valores de um conjunto de arquivos
def calcula_media(pasta_entrada, arquivos_entrada):
    arquivo_saida = 'resultado/Media-'+ pasta_entrada +'.txt'
    file = open(arquivo_saida, 'w+', encoding='utf-8')

    # le os arquivos de entrada e salva o resultado de cada um em um vetor
    vetor_resultados = []
    for i in range(len(arquivos_entrada)):
        path = 'resultado/'+ pasta_entrada + '/' + arquivos_entrada[i] + '.txt'
        vetor_resultados.append(le_arquivo(path))
    
    for i in range (5):
        for j in range(5):
            valores = []
            for resultado in vetor_resultados:
                valores.append(resultado[i][j])
            
            soma = sum(valores)
            media = soma / len(valores)
            #print('Media: '+ str(media))
            file.write(str(media) + '\n')

    file.close()
    print('Processamento das Médias de '+ pasta_entrada +' Concluído!\n--')

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
def constroi_grafico():
    arquivo_wer = 'resultado/Media-wer.txt'
    arquivo_tempos = 'resultado/Media-tempos.txt'
    
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

# Função que gera um arquivo de saída Final
def gera_arquivo_final(musicas):
    # Abre o arquivo para gravar os resultados
    arquivo_saida = open('Resultado Final.txt', 'w+', encoding='utf-8')
    arquivo_saida.write('RESULTADOS DAS MÚSICAS INDIVIDUALMENTE:\n\n')
    
    for musica in musicas:
        with open('resultado/wer/'+ musica +'.txt', 'r', encoding='utf-8') as file:
            result_wer = file.readlines()
        file.close()
        with open('resultado/tempos/'+ musica +'.txt', 'r', encoding='utf-8') as file:
            result_tempos = file.readlines()
        file.close()
        
        arquivo_saida.write('Música: '+ musica +'\n')
        
        modelos = ['tiny','base','small','medium','large']
        k = 0
        for modelo in modelos:
            arquivo_saida.write('\tModelo: '+ modelo +'\n')
            kbps = 64
            for i in range (5):
                linha = '\t\tTaxa de Bits: '+ str(kbps) +':\n\t\t\tTaxa de erro: '+ str(float(result_wer[k])) +'\n\t\t\tTempo de Processamento (segundos): '+ str(float(result_tempos[k])) +' \n'
                arquivo_saida.write(linha)
                k += 1
                kbps += 64
        
        arquivo_saida.write('\n')
    
    
    arquivo_saida.write('\n\n\nRESULTADO MÉDIO DAS MÚSICAS:\n\n')
    
    with open('resultado/wer/'+ musica +'.txt', 'r', encoding='utf-8') as file:
        result_wer = file.readlines()
    file.close()
    with open('resultado/tempos/'+ musica +'.txt', 'r', encoding='utf-8') as file:
        result_tempos = file.readlines()
    file.close()
    
    modelos = ['tiny','base','small','medium','large']
    k = 0
    for modelo in modelos:
        arquivo_saida.write('Modelo: '+ modelo +'\n')
        kbps = 64
        for i in range (5):
            linha = '\tTaxa de Bits: '+ str(kbps) +':\n\t\tTaxa de erro: '+ str(float(result_wer[k])) +'\n\t\tTempo de Processamento (segundos): '+ str(float(result_tempos[k])) +' \n'
            arquivo_saida.write(linha)
            k += 1
            kbps += 64
        
        arquivo_saida.write('\n')
    
    arquivo_saida.close()
    print('Processamento do arquivo Final Concluído!\n--')
    
# Função Main que executa o processo todo
def main():
    # Informar neste Array as músicas que serão processadas:
    # 1 - informar somente o 'Nome da Musica':
    # 2 - as músicas devem estar previamente nomeadas (na pasta 'audio/[kbps]/') no padrão exemplo: "Nome da Musica.mp3"
    musicas = ['Bohemian Rhapsody', 'Counting Stars', 'Summertime Sadness', 'The Sound of Silence', 'Wellerman']
    
    for musica in musicas:
        # Processa as músicas com Wisper (descomentar para executar)
        processa_musica(musica)
        # Calcula o WER das músicas processadas (descomentar para executar)
        calcula_erro(musica)
    
    # Calcula a média do WER das músicas processadas (descomentar para executar)
    calcula_media('wer', musicas)
    # Calcula a média do tempo de processamento das músicas processadas (descomentar para executar)
    calcula_media('tempos', musicas)

    # Mostra na tela o gráfico com as médias
    gera_arquivo_final(musicas)
    constroi_grafico()
    
# Executa a função Main
main()