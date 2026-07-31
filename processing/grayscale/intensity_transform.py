'''
Transformação logarítmica: Um mapeamento de pixels baseado na função matemática s = c * log(1 + r), que expande drasticamente a faixa de valores dos pixels escuros e
comprime a faixa dos pixels mais claros.
Vantagem: Reduz o range dinâmico de uma imagem de forma natural, trazendo à tona detalhes minuciosos que estavam completamente "escondidos" na escuridão, 
sem estourar as partes que já eram claras.
Principal Aplicação: Visualização do espectro de Fourier (cujos valores variam do zero ao infinito muito rapidamente), processamento de raios-X e astrofotografia.


Transformação de potência (Gamma): Um mapeamento curvo baseado na função exponencial s = c * (r ** gamma). Se gamma < 1, 
clareia a imagem alargando os tons escuros; se gamma > 1, escurece a imagem alargando os tons claros.

Vantagem: Permite um controle cirúrgico e bidirecional do contraste global da imagem.

Principal Aplicação: Correção de gamma em monitores e câmeras (para compensar a falha de exibição linear do hardware) e 
aprimoramento de contraste estético em fotografias digitais.

Fatiamento por intensidade: Uma ferramenta que destaca uma fatia de tons de cinza muito específica (entre uma faixa A e B) 
dentro do espectro, podendo atribuir um valor alto a essa fatia e zerar ou preservar o fundo original da imagem.

Vantagem: Isola características de interesse baseadas estritamente na sua luminosidade, separando o alvo do resto da imagem mantendo ou não o contexto visual.
'''

# Aqui não vou utilizar a biblioteca scipy por mais que pareça ser a melhor, para operações pontuais como essa ela adicionaria um peso não necessário
# então usar openCV que contém a ferramenta LUT que acelera o processo dos cálculos com os pixels 

import cv2
import numpy as np
from PIL import Image

# transformação logarítmica 
def log_transform(imagem: Image.Image, c: float) -> Image.Image:
    arr = np.array(imagem) 
    
    tabela = c * np.log(1 + np.arange(0, 256)) # mapeando os pixels baseado na função matemática e criando a tabela
    tabela = np.clip(tabela, 0, 255).astype(np.uint8) # converte a tabela para o formato de 8 bits (0 a 255)
    
    arr_processado = cv2.LUT(arr, tabela) # o openCV substitui os pixels da imagem instantaneamente usando a tabela (look up table LUT)
    
    return Image.fromarray(arr_processado)


def power_transform(imagem: Image.Image, c: float, gamma: float) -> Image.Image:
    arr = np.array(imagem)

    # normalizando (i/255.0) antes de aplicar a potência para evitar que números grandes estourem o limite e criando a tabela
    tabela = np.array([c * 255.0 * ((i / 255.0) ** gamma) for i in np.arange(0, 256)])

    # garante que os valores não passem de 255 nem caiam abaixo de 0
    tabela = np.clip(tabela, 0, 255).astype(np.uint8)

    # aplica a transformação
    arr_processado = cv2.LUT(arr, tabela)
    
    return Image.fromarray(arr_processado)


def intensity_slicing(imagem: Image.Image, a: int, b: int, preserve_bg: bool) -> Image.Image:
    arr = np.array(imagem)

    # máscara binária: pixels entre A e B viram 255, ou seja, branco e o resto vira 0
    mascara = cv2.inRange(arr, a, b)
    
    if preserve_bg:
        # cópia da imagem original
        arr_processado = np.copy(arr)
        # pinta de branco onde a máscara mostra que é verdadeiro
        arr_processado[mascara == 255] = 255
    else:
        # SE não for pra preservar o fundo, ele tem que ser preto 0
        # e isso se trata da nossa mascara 
        arr_processado = mascara
        
    return Image.fromarray(arr_processado)