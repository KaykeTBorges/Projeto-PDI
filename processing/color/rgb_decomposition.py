"""
Decomposição de uma imagem colorida em seus três componentes RGB
(Vermelho, Verde e Azul), cada um retornado como uma imagem
independente em escala de cinza (8-bit, modo 'L').
"""

from PIL import Image


def decompose_rgb(image: Image.Image) -> dict:
    """
    Recebe uma imagem colorida (modo 'RGB') e retorna um dicionário contendo
    as imagens correspondentes aos canais R, G e B, cada uma em escala de cinza (modo 'L').
    """

    # Força a conversão da imagem para o modo 'RGB' caso não esteja nesse modo.    
    if image.mode != "RGB":
        image = image.convert("RGB")

    canal_r, canal_g, canal_b = image.split()

    return {
        "R": canal_r,
        "G": canal_g,
        "B": canal_b,
    }