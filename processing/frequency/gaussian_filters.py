"""
Filtros gaussianos no domínio da frequência (passa-baixa e passa-alta).

Passa-baixa gaussiano: atenua altas frequências de forma suave, reduzindo
detalhes finos e ruídos sem o efeito de "ringing".

Passa-alta gaussiano: atenua baixas frequências, realçando bordas e
detalhes finos da imagem.

Ambos usam frequência de corte D₀ ajustável.
"""

from PIL import Image

from processing.frequency.fft_utils import (
    compute_fft,
    apply_filter_and_ifft,
    distance_matrix,
)


def gaussian_lowpass(imagem: Image.Image, cutoff: float) -> Image.Image:
    """
    Filtro passa-baixa gaussiano.

    H(u,v) = exp(-D(u,v)² / (2·D₀²))

    Args:
        imagem: PIL.Image grayscale.
        cutoff: frequência de corte D₀ (quanto maior, menos suavização)

    Returns:
        PIL.Image com as altas frequências atenuadas
    """
    fft_shifted = compute_fft(imagem)
    rows, cols = fft_shifted.shape
    D = distance_matrix(rows, cols)
    H = _gaussian_lp_kernel(D, cutoff)
    return apply_filter_and_ifft(fft_shifted, H)


def gaussian_highpass(imagem: Image.Image, cutoff: float) -> Image.Image:
    """
    Filtro passa-alta gaussiano.

    H(u,v) = 1 - exp(-D(u,v)² / (2·D₀²))

    Args:
        imagem: PIL.Image grayscale.
        cutoff: frequência de corte D₀ (quanto menor, mais bordas preservadas)

    Returns:
        PIL.Image com as baixas frequências atenuadas
    """
    fft_shifted = compute_fft(imagem)
    rows, cols = fft_shifted.shape
    D = distance_matrix(rows, cols)
    H = 1.0 - _gaussian_lp_kernel(D, cutoff)
    return apply_filter_and_ifft(fft_shifted, H)


def _gaussian_lp_kernel(D, cutoff: float):
    """Kernel gaussiano passa-baixa: exp(-D² / (2·D₀²))."""
    import numpy as np
    return np.exp(-(D ** 2) / (2.0 * cutoff ** 2))
