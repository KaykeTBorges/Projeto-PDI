"""
Equalização de histograma para imagens grayscale (modo 'L').

Retorna a imagem equalizada + os histogramas antes e depois,
que o app.py passa para o display.py exibir como gráfico de barras.
"""

import cv2
import numpy as np
from PIL import Image

from utils.image_io import pil_to_numpy, numpy_to_pil


def _histograma_normalizado(arr) -> list[float]:
    """Conta quantas vezes cada tom (0–255) aparece e divide pelo total de pixels."""
    counts = np.bincount(arr.ravel(), minlength=256).astype(float)
    total = counts.sum()
    return (counts / total).tolist() if total > 0 else [0.0] * 256


def equalize_histogram(
    imagem: Image.Image,
) -> tuple[Image.Image, list[float], list[float]]:
    """
    Equaliza o histograma de uma imagem grayscale.

    Parâmetros
    imagem : PIL.Image modo 'L'

    Retorno
    imagem_eq   : PIL.Image equalizada
    hist_antes  : list[float] — histograma normalizado original (256 valores)
    hist_depois : list[float] — histograma normalizado após equalização
    """
    if imagem.mode != "L":
        raise ValueError(
            f"Esperava imagem grayscale (modo 'L'), mas recebeu '{imagem.mode}'."
        )

    arr = pil_to_numpy(imagem)
    hist_antes = _histograma_normalizado(arr)

    arr_eq = cv2.equalizeHist(arr)
    hist_depois = _histograma_normalizado(arr_eq)

    return numpy_to_pil(arr_eq, modo="L"), hist_antes, hist_depois
