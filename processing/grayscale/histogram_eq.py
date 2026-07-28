"""
processing/grayscale/histogram_eq.py
--------------------------------------
Equalização de histograma para imagens grayscale (modo 'L').

Contrato com o app.py:
    equalize_histogram(img) -> (imagem_equalizada, hist_antes, hist_depois)

onde:
    - imagem_equalizada : PIL.Image no modo 'L'
    - hist_antes        : list[float] de 256 posições (frequências relativas)
    - hist_depois       : list[float] de 256 posições (frequências relativas)
"""

import numpy as np
from PIL import Image


def _compute_hist(arr: np.ndarray) -> list[float]:
    """Retorna histograma normalizado (frequências relativas) de array uint8."""
    counts = np.bincount(arr.ravel(), minlength=256).astype(float)
    total = counts.sum()
    if total == 0:
        return [0.0] * 256
    return (counts / total).tolist()


def equalize_histogram(
    imagem: Image.Image,
) -> tuple[Image.Image, list[float], list[float]]:
    """
    Aplica equalização de histograma a uma imagem grayscale.

    Parameters
    ----------
    imagem : PIL.Image
        Imagem no modo 'L' (grayscale 8-bit). Se o modo for diferente, uma
        ValueError é levantada — a sidebar já restringe este processo a
        imagens grayscale.

    Returns
    -------
    imagem_eq : PIL.Image
        Imagem equalizada, modo 'L'.
    hist_antes : list[float]
        Histograma normalizado (256 valores) antes da equalização.
    hist_depois : list[float]
        Histograma normalizado (256 valores) após a equalização.

    Raises
    ------
    ValueError
        Se a imagem não estiver no modo 'L'.
    """
    if imagem.mode != "L":
        raise ValueError(
            f"equalize_histogram: esperava imagem no modo 'L' (grayscale), "
            f"mas recebeu modo '{imagem.mode}'."
        )

    arr = np.array(imagem, dtype=np.uint8)

    # Histograma antes
    hist_antes = _compute_hist(arr)

    # CDF para calcular o mapeamento de intensidades
    hist_counts = np.bincount(arr.ravel(), minlength=256)
    cdf = hist_counts.cumsum()
    cdf_min = int(cdf[cdf > 0][0])   # menor valor não-nulo da CDF
    n_pixels = arr.size

    # Mapeamento de intensidades via fórmula clássica de equalização
    lut = np.round(
        (cdf - cdf_min) / (n_pixels - cdf_min) * 255
    ).clip(0, 255).astype(np.uint8)

    arr_eq = lut[arr]

    # Histograma depois
    hist_depois = _compute_hist(arr_eq)

    imagem_eq = Image.fromarray(arr_eq, mode="L")
    return imagem_eq, hist_antes, hist_depois
