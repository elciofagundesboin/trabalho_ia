# Importa a bilbioteca Jiwer
import jiwer

# Função que calcula o wer da música
def calcula_erro(musica):
    # abre o arquivo que irá gravar o WER
    caminho_saida = 'resultado/wer/'+ musica + '.txt'
    f_output = open(caminho_saida, "a+", encoding='utf-8')

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
            print ('------------------------')
            # grava o resultado no arquivo de saída
            f_output.write(str(wer) + '\n')
            kbps += 64
    # fecha o arquivo de saída
    f_output.close()
    
# Chama as funções para realizar os cálculos
#calcula_erro('Cuando Suba La Marea')
#calcula_erro('Faroeste Caboclo')
calcula_erro('Bohemian Rhapsody')
calcula_erro('Counting Stars')
calcula_erro('The Sound of Silence')
calcula_erro('Wellerman')
calcula_erro('Summertime Sadness')

'''
Estrutura do arquivo exportado com os resultados do WER:
O arquivo .txt exportado guarda em cada linha o resultado do WER para cada uma das situações, respectivamente:

    tiny 64kbps
    tiny 128kbps
    tiny 192kbps
    tiny 256kbps
    tiny 320kbps
    base 64kbps
    base 128kbps
    base 192kbps
    base 256kbps
    base 320kbps
    small 64kbps
    small 128kbps
    small 192kbps
    small 256kbps
    small 320kbps
    medium 64kbps
    medium 128kbps
    medium 192kbps
    medium 256kbps
    medium 320kbps
    large 64kbps
    large 128kbps
    large 192kbps
    large 256kbps
    large 320kbps

Para cada música é salvo um arquivo com os resultados dela mesma apenas.
'''