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
    linhas, colunas = arr.shape
    
    # Cria a matriz de saída
    out = np.copy(arr)
    
    # Para lidar com as bordas da imagem sem dar erro de índice,
    # fazemos um padding (preenchimento) espelhado usando o tamanho máximo necessário.
    pad_size = max_window // 2
    padded = np.pad(arr, pad_size, mode='reflect')
    
    # Percorre cada pixel da imagem original
    for i in range(linhas):
        for j in range(colunas):
            
            # Coordenadas ajustadas devido ao padding
            pi = i + pad_size
            pj = j + pad_size
            
            window_size = 3
            
            # Loop de expansão da janela (Nível A)
            while window_size <= max_window:
                w_pad = window_size // 2
                
                # Extrai a vizinhança atual
                window = padded[pi - w_pad : pi + w_pad + 1, pj - w_pad : pj + w_pad + 1]
                
                z_min = np.min(window)
                z_max = np.max(window)
                z_med = np.median(window)
                z_xy = padded[pi, pj]
                
                # Nível A: Verifica se a mediana NÃO é um ruído
                if z_min < z_med < z_max:
                    
                    # Nível B: Verifica se o próprio pixel NÃO é um ruído
                    if z_min < z_xy < z_max:
                        out[i, j] = z_xy  # Mantém o pixel original
                    else:
                        out[i, j] = z_med # Substitui pela mediana
                    
                    # Sai do loop while e vai para o próximo pixel da imagem
                    break 
                
                else:
                    # A mediana é um ruído. Aumenta a janela e repete Nível A.
                    window_size += 2
            
            # Se a janela estourou o limite máximo (max_window), 
            # entregamos a mediana da maior janela possível.
            else:
                out[i, j] = z_med
                
    return Image.fromarray(out)