"""
Máscara de aguçamento (unsharp masking): realça bordas e detalhes finos
da imagem, subtraindo uma versão borrada da imagem original
e somando essa diferença de volta, ponderada por um ganho.
"""

import numpy as np
from PIL import Image, ImageFilter


def _aguçar_array(arr: np.ndarray, gain: float, ksize: int) -> np.ndarray:
    """
    Aplica máscara de aguçamento a um array numpy representando uma imagem em escala de cinza.
    """
    imagem = Image.fromarray(arr.astype(np.uint8))
    borrada = imagem.filter(ImageFilter.BoxBlur(radius=ksize // 2))

    original_f = arr.astype(np.float32)
    borrada_f = np.array(borrada, dtype=np.float32)

    saida = original_f + gain * (original_f - borrada_f)
    return np.clip(saida, 0, 255).astype(np.uint8)


def sharpen(image: Image.Image, gain: float = 1.0, ksize: int = 3) -> Image.Image:
    """
    Aplica máscara de aguçamento à imagem, com o ganho e tamanho de kernel ajustáveis.
    """
    if ksize % 2 == 0:
        ksize += 1  # garante janela ímpar

    if image.mode == "L":
        arr = np.array(image)
        saida = _aguçar_array(arr, gain, ksize)
        return Image.fromarray(saida, mode="L")

    # RGB: aplica o aguçamento em cada canal separadamente e remonta
    imagem_rgb = image.convert("RGB")
    r, g, b = imagem_rgb.split()
    canais_processados = [
        _aguçar_array(np.array(c), gain, ksize) for c in (r, g, b)
    ]
    saida = np.stack(canais_processados, axis=-1)
    return Image.fromarray(saida, mode="RGB")