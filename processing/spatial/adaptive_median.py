# Filtro adaptativo de mediana (tamanho máximo da janela)
# Lembrar de modificar a UI para que esse filtro fique em FILTROS ESPACIAIS
"""
O filtro adaptativo de mediana é um algoritmo espacial 
que ajusta dinamicamente o tamanho de sua janela de busca baseado nas características locais da imagem, 
substituindo o pixel central apenas se ele for classificado como ruído impulsivo. Sua principal vantagem 
é a preservação extrema de bordas e detalhes finos (ao contrário do filtro estático que borra a imagem globalmente), 
sendo a ferramenta ideal para limpar ruído "sal e pimenta" de alta densidade em aplicações críticas como imagens 
médicas e sensoriamento remoto, onde perder nitidez original é inaceitável.

Altera o tamanho da janela local dinamicamente para preservar bordas
enquanto remove ruído de sal e pimenta de alta densidade.
"""

import numpy as np
from PIL import Image
import scipy.ndimage as ndimage

def adaptive_median(imagem: Image.Image, max_window: int) -> Image.Image:
    """
    Aplica o filtro adaptativo de mediana em uma imagem em tons de cinza.
    
    Parâmetros:
    imagem     : PIL.Image -> Imagem original (modo 'L').
    max_window : int -> Tamanho máximo permitido para a janela (deve ser ímpar).
    """
    # Garante que o tamanho máximo seja ímpar
    max_window = int(max_window)
    if max_window % 2 == 0:
        max_window += 1

    arr = np.array(imagem)
    out = np.copy(arr)
    
    # Máscara booleana para rastrear quais pixels ainda precisam ser processados
    # Começa com True (Verdadeiro) para todos os pixels
    pixels_pendentes = np.ones_like(arr, dtype=bool)
    
    # Loop baseado no tamanho da janela, pulando de 2 em 2 (3, 5, 7...)
    for w in range(3, max_window + 1, 2):
        
        # Se não há mais pixels pendentes, podemos parar o processamento cedo
        if not np.any(pixels_pendentes):
            break
            
        # O SciPy calcula min, max e mediana para a imagem INTEIRA de uma vez
        z_min = ndimage.minimum_filter(arr, size=w)
        z_max = ndimage.maximum_filter(arr, size=w)
        z_med = ndimage.median_filter(arr, size=w)
        
        # Nível A: Verifica se a mediana NÃO é um ruído
        # Compara as matrizes inteiras simultaneamente
        nivel_a_passou = (z_med > z_min) & (z_med < z_max)
        
        # Nível B: Verifica se o próprio pixel NÃO é um ruído original
        nivel_b_passou = (arr > z_min) & (arr < z_max)
        
        # Condição 1: A passou e B passou -> Mantém o pixel original
        manter_original = nivel_a_passou & nivel_b_passou & pixels_pendentes
        
        # Condição 2: A passou, mas B falhou -> Substitui pela mediana
        usar_mediana = nivel_a_passou & (~nivel_b_passou) & pixels_pendentes
        
        # Aplica as decisões apenas nos pixels que satisfizeram as condições
        out[manter_original] = arr[manter_original]
        out[usar_mediana] = z_med[usar_mediana]
        
        # Marca esses pixels como "resolvidos" (False) para as próximas iterações
        pixels_pendentes[manter_original | usar_mediana] = False

    # Se a janela estourou o limite máximo (max_window) e ainda sobraram pixels pendentes,
    # entregamos a mediana da maior janela possível para eles.
    if np.any(pixels_pendentes):
        out[pixels_pendentes] = z_med[pixels_pendentes]
                
    return Image.fromarray(out)