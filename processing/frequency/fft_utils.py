"""
Utilitários de FFT para os filtros de frequência.

Fornece funções para transformar uma imagem PIL para o domínio da
frequência (via np.fft), aplicar um filtro H(u,v) e retornar ao
domínio espacial como PIL.Image.
"""

import numpy as np
from PIL import Image


def compute_fft(imagem: Image.Image) -> np.ndarray:
    """
    Converte uma imagem PIL grayscale para o domínio da frequência.

    Retorna o espectro centralizado (fftshift aplicado), pronto para
    multiplicação por um filtro H(u,v).
    """
    arr = np.array(imagem, dtype=np.float64)
    fft = np.fft.fft2(arr)
    return np.fft.fftshift(fft)


def apply_filter_and_ifft(fft_shifted: np.ndarray, H: np.ndarray) -> Image.Image:
    """
    Multiplica o espectro centrado pelo filtro H, faz a IFFT e retorna
    uma PIL.Image grayscale (uint8, [0–255]).
    """
    filtered = fft_shifted * H
    resultado = np.fft.ifft2(np.fft.ifftshift(filtered))
    resultado = np.abs(resultado)
    resultado = np.clip(resultado, 0, 255).astype(np.uint8)
    return Image.fromarray(resultado, mode="L")


def distance_matrix(rows: int, cols: int) -> np.ndarray:
    """
    Gera a matriz D(u,v) com a distância euclidiana de cada ponto ao
    centro do espectro. Dimensão: (rows, cols).
    """
    u = np.arange(rows) - rows // 2
    v = np.arange(cols) - cols // 2
    V, U = np.meshgrid(v, u)
    return np.sqrt(U**2 + V**2)
