# Filtros de suavização
# Os filtro de suavização se tratam dos seguintes 
'''
Filtro de média gaussiana: Um filtro espacial que suaviza a imagem dando pesos diferentes 
aos pixels vizinhos (maior peso no centro). É muito utilizado para atenuar ruídos de distribuição normal (gaussiano).

Vantagem: Ele suaviza a imagem de forma muito mais natural do que a média simples, 
preservando um pouco melhor as bordas e evitando o efeito de "blocos" (artefatos de ringing).

Principal Aplicação: Remoção de ruído Gaussiano (ruído de sensor) e 
preparação de imagens para algoritmos de detecção de bordas (como o algoritmo de Canny).

Filtro de mediana: Um filtro não linear espacial excelente para remover ruído impulsivo (como o ruído "sal e pimenta"), 
preservando as bordas da imagem de forma muito mais eficaz do que o filtro de média. (Nota: Os filtros de mínimo e máximo 
também pertencem à mesma família de estatística de ordem, 
mas são geralmente usados para operações morfológicas de erosão e dilatação, respectivamente, mais do que para suavização geral).

Vantagem: Como ele não cria novos valores (apenas seleciona um valor existente na vizinhança), 
as bordas nítidas da imagem não são borradas como ocorre nos filtros de média.

Principal Aplicação: É a ferramenta definitiva para remover o ruído "sal e pimenta" (ruído impulsivo),
que se manifesta como pixels aleatórios completamente pretos ou brancos espalhados pela imagem.


Filtro de mínimo: O filtro de mínimo é um filtro não-linear que atua de forma semelhante à operação morfológica de erosão em imagens em tons de cinza.

Vantagem e Efeito: O resultado visual é que os objetos escuros da imagem aumentam de tamanho, 
enquanto os objetos claros diminuem ou desaparecem.

Principal Aplicação: É utilizado para eliminar pequenos detalhes brilhantes (ruídos claros) em um fundo escuro, 
ou para separar objetos claros que estão levemente conectados.

Filtro de máximo: 
O filtro de máximo é o oposto do filtro de mínimo, sendo um filtro não-linear relacionado à operação morfológica de dilatação.

Vantagem e Efeito: Visualmente, os objetos claros se expandem (dilatam) e os objetos escuros encolhem.

Principal Aplicação: É excelente para preencher pequenos "buracos" escuros dentro de regiões claras ou eliminar pequenos ruídos escuros 
(como o ruído "pimenta") em um fundo claro. 
Também é usado para conectar elementos brilhantes que estão quebrados ou segmentados.
'''


import numpy as np
from PIL import Image
import scipy.ndimage as ndimage

# lembrar de modificar o código para a função de kayke

def gaussian_mean(imagem: Image.Image, sigma: float, ksize: int) -> Image.Image:
    # O SciPy calcula o tamanho do kernel automaticamente com base no sigma.
    # Mantemos ksize na assinatura para não quebrar a compatibilidade com o sidebar.py.
    arr = np.array(imagem) 
    
    # Se a imagem for RGB (3 dimensões), aplicamos o sigma apenas em X e Y, e 0 no canal de cores.
    if arr.ndim == 3:
        sigmas = (float(sigma), float(sigma), 0.0)
    else:
        sigmas = float(sigma)
        
    arr_processado = ndimage.gaussian_filter(arr, sigma=sigmas)
    return Image.fromarray(arr_processado)

def median_filter(imagem: Image.Image, ksize: int) -> Image.Image:
    ksize = int(ksize)
    if ksize % 2 == 0: ksize += 1

    arr = np.array(imagem)
    
    # Previne que o filtro misture os canais RGB
    tamanho_janela = (ksize, ksize, 1) if arr.ndim == 3 else (ksize, ksize)
    
    arr_processado = ndimage.median_filter(arr, size=tamanho_janela)
    return Image.fromarray(arr_processado)

def min_filter(imagem: Image.Image, ksize: int) -> Image.Image:
    ksize = int(ksize)
    if ksize % 2 == 0: ksize += 1

    arr = np.array(imagem)
    
    tamanho_janela = (ksize, ksize, 1) if arr.ndim == 3 else (ksize, ksize)
    
    # O minimum_filter do SciPy tem o exato mesmo efeito da Erosão no OpenCV
    arr_processado = ndimage.minimum_filter(arr, size=tamanho_janela)
    return Image.fromarray(arr_processado)

def max_filter(imagem: Image.Image, ksize: int) -> Image.Image:
    ksize = int(ksize)
    if ksize % 2 == 0: ksize += 1

    arr = np.array(imagem)
    
    tamanho_janela = (ksize, ksize, 1) if arr.ndim == 3 else (ksize, ksize)
    
    # O maximum_filter do SciPy tem o exato mesmo efeito da Dilatação no OpenCV
    arr_processado = ndimage.maximum_filter(arr, size=tamanho_janela)
    return Image.fromarray(arr_processado)