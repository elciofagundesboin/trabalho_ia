# Importa o modelo Wisper
import whisper

# Função para calcular
def processa_musica(musica):
    modelos = ['tiny','base','small','medium','large']
    for modelo in modelos:
        kbps = 64
        for i in range (5):
            # ---
            # Carrega o modelo
            model = whisper.load_model(modelo)
            # Processa a música
            local_musica = 'audio/'+ str(kbps) +'/'+ musica +'.mp3'
            result = model.transcribe(local_musica)
            # Abre o arquivo de saída em modo leitura
            arquivo_saida = musica +'-'+ str(kbps) +'-'+ modelo +'.txt'
            file = open('saida/'+ arquivo_saida, 'w+', encoding='utf-8')
            # Escreve no arquivo o texto gerado
            file.write(result['text'])
            # Fecha o arquivo
            file.close()
            #print(local_musica)
            #print(arquivo_saida)
            print('Processado: '+ modelo +' | '+ local_musica)
            print ('------------------------')
            # ---
            kbps += 64

# Processa as músicas:
# Observações:
# 1 - informar somente o 'Nome da Musica':
# 2 - as músicas devem estar previamente nomeadas (na pasta 'audio/[kbps]/') no padrão exemplo: "Nome da Musica.mp3"
processa_musica('Faroeste Caboclo')
processa_musica('Cuando Suba La Marea')