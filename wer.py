# Importa a bilbioteca Jiwer
import jiwer

# Função que calcula o wer da música
def calcula_erro(musica):
    kbps = 64
    for i in range (5):
        # ---
        # abre o arquivo que irá gravar o WER
        caminho_saida = 'resultado/WER-'+ musica + '-'+ str(kbps) +'.txt'
        f_output = open(caminho_saida, "a+", encoding='utf-8')

        # abre o arquivo com o texto original (letra)
        caminho_origem = 'letras/'+ musica +' - Letra.txt'
        f_origem = open(caminho_origem, 'r', encoding='utf-8')
        texto_origem = f_origem.read()
        f_origem.close()
        
        modelos = ['tiny','base','small','medium','large']
        for modelo in modelos:
            # abre o arquivo com o texto de hipotese (resultado do wisper)
            caminho_hipotese = 'saida/'+ musica +'-'+ str(kbps) +'-'+ modelo + '.txt'
            f_hipotese = open(caminho_hipotese, 'r', encoding='utf-8')
            texto_hipotese = f_hipotese.read()
            f_hipotese.close()

            # calcula o WER (nesta etapa remove alguns espaços "em branco", como quebras de linha)
            measures = jiwer.compute_measures(jiwer.RemoveWhiteSpace(replace_by_space=True)(texto_origem), texto_hipotese)
            wer = measures['wer']
            # imprime na tela e grava o resultado do WER no arquivo de saída
            print('WER ('+ caminho_origem +')('+ caminho_hipotese +'): '+ str(wer))
            print ('------------------------')
            f_output.write(str(wer) + '\n')

        # fecha o arquivo de saída
        f_output.close()
        # ---
        kbps += 64

# Chama as funções para realizar os cálculos
calcula_erro('Faroeste Caboclo')
calcula_erro('Cuando Suba La Marea')