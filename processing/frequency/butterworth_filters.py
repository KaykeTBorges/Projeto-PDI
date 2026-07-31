"""
Filtros de Butterworth no domínio da frequência (passa-baixa e passa-alta).

Passa-baixa de Butterworth: atenua altas frequências com uma transição
controlada pela ordem n. Ordem baixa → transição suave (sem ringing);
ordem alta → transição abrupta (pode gerar ringing).

Passa-alta de Butterworth: atenua baixas frequências, realçando bordas
e detalhes, com a mesma flexibilidade de controle pela ordem.

Ambos usam frequência de corte D₀ e ordem n ajustáveis.
"""

import numpy as np
from PIL import Image

from processing.frequency.fft_utils import (
    compute_fft,
    apply_filter_and_ifft,
    distance_matrix,
)


def butterworth_lowpass(imagem: Image.Image, cutoff: float, order: int) -> Image.Image:
    """
    Filtro passa-baixa de Butterworth.

    H(u,v) = 1 / (1 + (D(u,v)/D₀)^(2n))

    Args:
        imagem: PIL.Image grayscale
        cutoff: frequência de corte D₀
        order:  ordem n do filtro (controla a inclinação da transição)

    Returns:
        PIL.Image com as altas frequências atenuadas
    """
    fft_shifted = compute_fft(imagem)
    rows, cols = fft_shifted.shape
    D = distance_matrix(rows, cols)
    H = _butterworth_lp_kernel(D, cutoff, order)
    return apply_filter_and_ifft(fft_shifted, H)


def butterworth_highpass(imagem: Image.Image, cutoff: float, order: int) -> Image.Image:
    """
    Filtro passa-alta de Butterworth.

    H(u,v) = 1 - 1 / (1 + (D(u,v)/D₀)^(2n))

    Args:
        imagem: PIL.Image grayscale
        cutoff: frequência de corte D₀
        order:  ordem n do filtro

    Returns:
        PIL.Image com as baixas frequências atenuadas
    """
    fft_shifted = compute_fft(imagem)
    rows, cols = fft_shifted.shape
    D = distance_matrix(rows, cols)
    H = 1.0 - _butterworth_lp_kernel(D, cutoff, order)
    return apply_filter_and_ifft(fft_shifted, H)


def _butterworth_lp_kernel(D: np.ndarray, cutoff: float, order: int) -> np.ndarray:
    """Kernel passa-baixa de Butterworth: 1 / (1 + (D/D₀)^(2n))."""
    return 1.0 / (1.0 + (D / cutoff) ** (2 * order))
