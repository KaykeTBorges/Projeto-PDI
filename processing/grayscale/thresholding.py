
'''
Limiarização ou Binarização de imagens: Uma transformação não-linear que converte uma imagem em tons de cinza para uma imagem binária (estritamente preta e branca).
Avalia cada pixel contra um limiar de corte 'k', transformando em branco os valores acima de 'k' e em preto os valores menores ou iguais a 'k'.
Vantagem: Algoritmo extremamente rápido que divide categoricamente a imagem em duas regiões (o que é objeto e o que é fundo).
'''

import cv2
import numpy as np
from PIL import Image


def threshold(imagem: Image.Image, k: int) -> Image.Image:
    arr = np.array(imagem)
    # usando a função já pronta da biblioteca
    # retorna dois valores 
    # o primeiro vai ser o limiar e o segundo a imagem em si processada
    _, arr_processado = cv2.threshold(arr, k, 255, cv2.THRESH_BINARY)
    
    return Image.fromarray(arr_processado)