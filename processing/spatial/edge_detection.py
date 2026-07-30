"""
Operações espaciais para detecção de bordas e realce.

Inclui:
- Máscara de aguçamento (unsharp mask) com ganho e janela ajustáveis.
- Realce por Laplaciano com janela ajustável.
- Gradiente de Sobel.
"""

import numpy as np
from PIL import Image, ImageFilter


def _odd_ksize(ksize: int) -> int:
	"""Garante tamanho de janela ímpar e mínimo 3."""
	ksize = int(max(3, ksize))
	return ksize if ksize % 2 == 1 else ksize + 1


def _convolve2d(arr: np.ndarray, kernel: np.ndarray) -> np.ndarray:
	"""Convolução 2D simples com padding refletido."""
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


def _unsharp_array(arr: np.ndarray, gain: float, ksize: int) -> np.ndarray:
	"""Aplica máscara de aguçamento em uma imagem 2D (canal único)."""
	imagem = Image.fromarray(arr.astype(np.uint8), mode="L")
	borrada = imagem.filter(ImageFilter.BoxBlur(radius=ksize // 2))

	original_f = arr.astype(np.float32)
	borrada_f = np.array(borrada, dtype=np.float32)

	saida = original_f + float(gain) * (original_f - borrada_f)
	return np.clip(saida, 0, 255).astype(np.uint8)


def sharpen_mask(image: Image.Image, gain: float = 1.0, ksize: int = 3) -> Image.Image:
	"""
	Máscara de aguçamento com ganho e tamanho de janela ajustáveis.
	"""
	ksize = _odd_ksize(ksize)

	if image.mode == "L":
		arr = np.array(image)
		return Image.fromarray(_unsharp_array(arr, gain, ksize), mode="L")

	imagem_rgb = image.convert("RGB")
	canais = imagem_rgb.split()
	processados = [_unsharp_array(np.array(c), gain, ksize) for c in canais]
	saida = np.stack(processados, axis=-1)
	return Image.fromarray(saida, mode="RGB")


def laplacian(image: Image.Image, ksize: int = 3) -> tuple[Image.Image, Image.Image]:
	"""
	Realce por Laplaciano com janela ajustável.

	Retorna:
	- imagem realçada
	- resposta laplaciana (para visualização)
	"""
	ksize = _odd_ksize(ksize)
	arr = np.array(image.convert("L"), dtype=np.float32)

	kernel = np.ones((ksize, ksize), dtype=np.float32)
	kernel[ksize // 2, ksize // 2] = -(ksize * ksize - 1)

	lap = _convolve2d(arr, kernel)
	realcada = np.clip(arr - lap, 0, 255).astype(np.uint8)

	lap_abs = np.abs(lap)
	if lap_abs.max() > 0:
		lap_vis = (lap_abs / lap_abs.max()) * 255.0
	else:
		lap_vis = lap_abs

	return Image.fromarray(realcada, mode="L"), Image.fromarray(lap_vis.astype(np.uint8), mode="L")


def sobel(image: Image.Image, ksize: int = 3) -> Image.Image:
	"""
	Gradiente de Sobel.

	Se `ksize` for maior que 3, aplica uma suavização média antes do Sobel,
	usando a janela informada.
	"""
	ksize = _odd_ksize(ksize)
	arr = np.array(image.convert("L"), dtype=np.float32)

	if ksize > 3:
		kernel_suav = np.ones((ksize, ksize), dtype=np.float32) / float(ksize * ksize)
		arr = _convolve2d(arr, kernel_suav)

	kx = np.array([
		[-1, 0, 1],
		[-2, 0, 2],
		[-1, 0, 1],
	], dtype=np.float32)
	ky = np.array([
		[-1, -2, -1],
		[0, 0, 0],
		[1, 2, 1],
	], dtype=np.float32)

	gx = _convolve2d(arr, kx)
	gy = _convolve2d(arr, ky)
	mag = np.hypot(gx, gy)

	if mag.max() > 0:
		mag = (mag / mag.max()) * 255.0

	return Image.fromarray(np.clip(mag, 0, 255).astype(np.uint8), mode="L")
