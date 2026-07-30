"""
Máscara de aguçamento (unsharp masking): realça bordas e detalhes finos
da imagem, subtraindo uma versão borrada da imagem original
e somando essa diferença de volta, ponderada por um ganho.
"""

import numpy as np
from PIL import Image


def _convolve2d(arr: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Convolução 2D com padding refletido."""
    kh, kw = kernel.shape
    pad_h = kh // 2
    pad_w = kw // 2

    padded = np.pad(arr, ((pad_h, pad_h), (pad_w, pad_w)), mode="reflect")
    out = np.zeros_like(arr, dtype=np.float32)

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            region = padded[i : i + kh, j : j + kw]
            out[i, j] = float(np.sum(region * kernel))

    return out


def _blur_mean(arr: np.ndarray, ksize: int) -> np.ndarray:
    """Borramento por média com kernel quadrado ksize x ksize."""
    kernel = np.ones((ksize, ksize), dtype=np.float32) / float(ksize * ksize)
    return _convolve2d(arr.astype(np.float32), kernel)


def _agucar_array(arr: np.ndarray, gain: float, ksize: int) -> np.ndarray:
    """
    Aplica máscara de aguçamento a um array numpy representando uma imagem em escala de cinza.
    """
    original_f = arr.astype(np.float32)
    borrada_f = _blur_mean(arr, ksize)

    saida = original_f + gain * (original_f - borrada_f)
    return np.clip(saida, 0, 255).astype(np.uint8)


def sharpen(image: Image.Image, gain: float = 1.0, ksize: int = 3) -> Image.Image:
    """
    Aplica máscara de aguçamento à imagem, com o ganho e tamanho de kernel ajustáveis.
    """
    if ksize < 3 or ksize % 2 == 0:
        raise ValueError("ksize deve ser ímpar e maior ou igual a 3.")

    if image.mode == "L":
        arr = np.array(image)
        saida = _agucar_array(arr, gain, ksize)
        return Image.fromarray(saida, mode="L")

    # RGB: aplica o aguçamento em cada canal separadamente e remonta
    imagem_rgb = image.convert("RGB")
    r, g, b = imagem_rgb.split()
    canais_processados = [
        _agucar_array(np.array(c), gain, ksize) for c in (r, g, b)
    ]
    saida = np.stack(canais_processados, axis=-1)
    return Image.fromarray(saida, mode="RGB")