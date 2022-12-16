# Importa o modelo Wisper
import whisper
# Importa as bibliotecas de time
import time
import timeit

# Função para calcular
def processa_musica(musica):
    # abre o arquivo que irá gravar o WER
    caminho_saida = 'resultado/tempos/'+ musica +'.txt'
    f_output = open(caminho_saida, "a+", encoding='utf-8')

    modelos = ['tiny','base','small','medium','large']
    tempos = []
    for modelo in modelos:
        kbps = 64
        tempo = []
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
            #print(local_musica)
            #print(arquivo_saida)
            tempo.append(fim - inicio)
            print('Processado: '+ modelo +' | '+ local_musica)
            print('Tempo de execução: '+ str(fim - inicio) +' segundos')
            print ('------------------------')
            # ---
            kbps += 64
        tempos.append(tempo)
    # grava o resultado no arquivo de saída
    f_output.write(str(tempos) + '\n')
    # fecha o arquivo de saída
    f_output.close()

# Processa as músicas:
# Observações:
# 1 - informar somente o 'Nome da Musica':
# 2 - as músicas devem estar previamente nomeadas (na pasta 'audio/[kbps]/') no padrão exemplo: "Nome da Musica.mp3"
#processa_musica('Faroeste Caboclo')
processa_musica('Cuando Suba La Marea')