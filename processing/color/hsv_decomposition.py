"""
Decomposição de uma imagem colorida em seus três componentes HSV
(Matiz, Saturação e Valor), cada um retornado como uma imagem
independente em escala de cinza (8-bit, modo 'L').
"""

from PIL import Image


def decompose_hsv(image: Image.Image) -> dict:
    """
    Decomposição de uma imagem colorida em seus três componentes HSV.
    Recebe uma imagem colorida (modo 'RGB') e retorna um dicionário contendo 
    As imagens correspondentes aos canais H, S e V, cada uma em escala de cinza (modo 'L').
    """
    if image.mode != "RGB":
        image = image.convert("RGB")

    imagem_hsv = image.convert("HSV")
    canal_h, canal_s, canal_v = imagem_hsv.split()

    return {
        "H": canal_h,
        "S": canal_s,
        "V": canal_v,
    }