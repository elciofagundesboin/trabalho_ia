# Importa a bilbioteca Jiwer
import jiwer

# Função que calcula o wer da música
def calcula_erro(musica):
    # abre o arquivo que irá gravar o WER
    caminho_saida = 'resultado/wer/'+ musica + '.txt'
    f_output = open(caminho_saida, "a+", encoding='utf-8')

    modelos = ['tiny','base','small','medium','large']
    saidas = []
    for modelo in modelos:
        # abre o arquivo com o texto original (letra)
        caminho_origem = 'letras/'+ musica +' - Letra.txt'
        f_origem = open(caminho_origem, 'r', encoding='utf-8')
        texto_origem = f_origem.read()
        f_origem.close()
        
        kbps = 64
        saida = []
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
            saida.append(wer)
            kbps += 64
        saidas.append(saida)
    # grava o resultado no arquivo de saída
    f_output.write(str(saida) + '\n')
    # fecha o arquivo de saída
    f_output.close()
        

# Chama as funções para realizar os cálculos
calcula_erro('Faroeste Caboclo')
calcula_erro('Cuando Suba La Marea')