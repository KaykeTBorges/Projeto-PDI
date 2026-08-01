"""
Operações espaciais para detecção de bordas e realce (Versão Otimizada).

Inclui:
- Máscara de aguçamento (unsharp mask) com ganho e janela ajustáveis.
- Realce por Laplaciano com janela ajustável.
- Gradiente de Sobel com janela ajustável.
"""

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage


def _odd_ksize(ksize: int) -> int:
    """Garante tamanho de janela ímpar e mínimo 3."""
    ksize = int(max(3, ksize))
    return ksize if ksize % 2 == 1 else ksize + 1


def _unsharp_array(arr: np.ndarray, gain: float, ksize: int) -> np.ndarray:
    """Aplica máscara de aguçamento otimizada em 2D ou RGB (in-place math)."""
    original_f = arr.astype(np.float32, copy=False)

    # axes=(0, 1) faz o filtro ser 2D espacial, evitando o overhead do filtro 3D no RGB
    axes_to_filter = (0, 1) if original_f.ndim == 3 else None
    borrada_f = ndimage.uniform_filter(
        original_f,
        size=ksize,
        mode="mirror",
        axes=axes_to_filter,
    )

    saida = original_f
    saida *= 1.0 + float(gain)
    saida -= float(gain) * borrada_f

    return np.clip(saida, 0, 255, out=saida).astype(np.uint8)


def sharpen_mask(image: Image.Image, gain: float = 1.0, ksize: int = 3) -> Image.Image:
    """Máscara de aguçamento com ganho e tamanho de janela ajustáveis."""
    ksize = _odd_ksize(ksize)
    mode = image.mode

    if mode not in ("L", "RGB"):
        image = image.convert("RGB")
        mode = "RGB"

    arr = np.array(image)
    saida = _unsharp_array(arr, gain, ksize)
    return Image.fromarray(saida, mode=mode)


def laplacian(image: Image.Image, ksize: int = 3) -> tuple[Image.Image, Image.Image]:
    """
    Realce por Laplaciano com janela ajustável.

    O ganho é normalizado para o kernel clássico 3x3 (fator 9), independente
    do tamanho da janela escolhida, evitando saturação para ksize > 3.

    Retorna:
    - imagem realçada
    - resposta laplaciana (para visualização)
    """
    ksize = _odd_ksize(ksize)

    arr = np.array(
        image.convert("L") if image.mode != "L" else image, dtype=np.float32
    )

    # Ganho fixo (referência: kernel laplaciano clássico 3x3),
    # independente do tamanho real da janela usada para calcular a média local.
    GANHO_REFERENCIA = 9.0

    media = ndimage.uniform_filter(arr, size=ksize, mode="mirror")

    # lap = (arr - media) * ganho  -> resposta laplaciana (bordas positivas/negativas)
    lap = arr - media
    lap *= GANHO_REFERENCIA

    # Realçada: arr + lap (soma o componente de alta frequência de volta à imagem)
    realcada = arr + lap
    np.clip(realcada, 0, 255, out=realcada)

    # Resposta Laplaciana para visualização (Normalização min-max robusta)
    lap_abs = np.abs(lap)
    max_val = lap_abs.max()
    if max_val > 0:
        lap_abs *= 255.0 / max_val

    return Image.fromarray(realcada.astype(np.uint8), mode="L"), Image.fromarray(
        lap_abs.astype(np.uint8), mode="L"
    )


def _sobel_ksize(ksize: int) -> int:
    """
    Garante ksize ímpar dentro do intervalo suportado pelo cv2.Sobel: [3, 7].
    """
    ksize = _odd_ksize(ksize)
    return min(ksize, 7)


def sobel(image: Image.Image, ksize: int = 3) -> Image.Image:
    """
    Calcula a magnitude do gradiente de Sobel usando cv2.Sobel.
    Janela ajustável, limitada ao intervalo suportado pelo OpenCV: 3, 5 ou 7.
    """
    ksize = _sobel_ksize(ksize)

    arr = np.array(
        image.convert("L") if image.mode != "L" else image, dtype=np.float32
    )

    gx = cv2.Sobel(arr, cv2.CV_32F, 1, 0, ksize=ksize, borderType=cv2.BORDER_REFLECT)
    gy = cv2.Sobel(arr, cv2.CV_32F, 0, 1, ksize=ksize, borderType=cv2.BORDER_REFLECT)

    # Magnitude: sqrt(gx^2 + gy^2)
    mag = np.hypot(gx, gy)

    # Normalização 0-255 in-place
    max_val = mag.max()
    if max_val > 0:
        mag *= 255.0 / max_val

    return Image.fromarray(mag.astype(np.uint8), mode="L")