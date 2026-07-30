"""
Geração de ruídos espaciais:
- Ruído Aditivo Gaussiano
- Ruído Sal e Pimenta (com proporções ajustáveis)

Compatível com a interface do Streamlit (retorna PIL.Image).
"""

import numpy as np
from PIL import Image


def gaussian_noise(imagem: Image.Image, mean: float, std: float) -> Image.Image:
    """
    Adiciona ruído gaussiano à imagem.
    
    Parâmetros:
    mean : float -> Média da distribuição (deslocamento de intensidade).
    std  : float -> Desvio padrão (força do ruído).
    """
    arr = np.array(imagem)
    
    # Gera a matriz de ruído com as mesmas dimensões da imagem (incluindo canais de cor)
    ruido = np.random.normal(mean, std, arr.shape)
    
    # Soma o ruído à imagem original
    arr_ruidoso = arr + ruido
    
    # Garante que os valores permaneçam no intervalo válido de 8-bits [0, 255]
    arr_clipado = np.clip(arr_ruidoso, 0, 255).astype(np.uint8)
    
    return Image.fromarray(arr_clipado)


def salt_pepper(imagem: Image.Image, amount: float, salt_vs_pepper: float) -> Image.Image:
    """
    Adiciona ruído Sal (branco) e/ou Pimenta (preto) à imagem.
    
    Parâmetros:
    amount         : float -> Proporção total de pixels afetados (ex: 0.05 = 5%).
    salt_vs_pepper : float -> Balanço entre sal e pimenta (1.0 = só sal, 0.0 = só pimenta).
    """
    arr = np.array(imagem)
    # Criamos uma cópia para não alterar o array original por referência
    out = np.copy(arr)
    
    # Pega apenas as dimensões espaciais (linhas e colunas), ignorando canais de cor se for RGB
    linhas, colunas = arr.shape[:2]
    total_pixels = linhas * colunas
    
    # Calcula a quantidade exata de pixels de sal e de pimenta
    num_salt = int(total_pixels * amount * salt_vs_pepper)
    num_pepper = int(total_pixels * amount * (1.0 - salt_vs_pepper))
    
    # --- Aplica o ruído SAL (Pixels Brancos: 255) ---
    if num_salt > 0:
        # Sorteia coordenadas X e Y aleatórias
        coords_x = np.random.randint(0, linhas, num_salt)
        coords_y = np.random.randint(0, colunas, num_salt)
        # Se a imagem for RGB, atribuir 255 aqui deixa os 3 canais brancos automaticamente
        out[coords_x, coords_y] = 255
        
    # --- Aplica o ruído PIMENTA (Pixels Pretos: 0) ---
    if num_pepper > 0:
        # Sorteia coordenadas X e Y aleatórias
        coords_x = np.random.randint(0, linhas, num_pepper)
        coords_y = np.random.randint(0, colunas, num_pepper)
        out[coords_x, coords_y] = 0
        
    return Image.fromarray(out)