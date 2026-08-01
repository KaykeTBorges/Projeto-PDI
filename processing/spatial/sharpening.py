"""
Filtro espacial de aguçamento (Sharpening) de imagem via Máscara de Aguçamento (Unsharp Masking).

Suporta imagens em tons de cinza (L) e coloridas (RGB).
Usa suavização por média móvel acelerada via OpenCV para extrair as altas frequências 
da imagem. Como a média é normalizada no domínio espacial pelo tamanho do kernel (ksize x ksize), 
o ganho é mantido consistente e a imagem não sofre saturação ao aumentar o tamanho da janela.
"""


import cv2
import numpy as np
from PIL import Image


def sharpen_fast(
    image: Image.Image, gain: float = 1.0, ksize: int = 3
) -> Image.Image:
    ksize = int(ksize)
    if ksize < 3 or ksize % 2 == 0:
        raise ValueError("ksize deve ser ímpar e maior ou igual a 3.")

    mode = image.mode
    if mode not in ("L", "RGB"):
        image = image.convert("RGB")
        mode = "RGB"

    arr = np.array(image)

    # O OpenCV blur é mais rápido que o uniform_filter do SciPy, especialmente para imagens grandes.
    borrada = cv2.blur(arr, (ksize, ksize), borderType=cv2.BORDER_REFLECT_101)

    saida = cv2.addWeighted(arr, 1.0 + gain, borrada, -gain, 0)

    return Image.fromarray(saida, mode=mode)


def sharpen(image: Image.Image, gain: float = 1.0, ksize: int = 3) -> Image.Image:
    """Aplica máscara de aguçamento usando a implementação otimizada."""
    return sharpen_fast(image, gain, ksize)
