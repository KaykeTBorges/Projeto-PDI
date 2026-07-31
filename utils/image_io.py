"""
Utilitários de I/O de imagens e conversão PIL ↔ NumPy.
"""

import io
import numpy as np
from PIL import Image


def load_image(arquivo) -> Image.Image:
    """Abre um arquivo de imagem (upload do Streamlit ou caminho em disco)."""
    try:
        imagem = Image.open(arquivo)
        imagem.load()
        return imagem
    except Exception as e:
        raise ValueError(f"Não foi possível abrir a imagem: {e}")


def pil_to_numpy(imagem: Image.Image) -> np.ndarray:
    """Converte PIL.Image para array NumPy uint8."""
    return np.array(imagem, dtype=np.uint8)


def numpy_to_pil(arr: np.ndarray, modo: str | None = None) -> Image.Image:
    """
    Converte array NumPy para PIL.Image.

    Se não informar o modo, o PIL tenta detectar automaticamente
    (funciona bem para arrays 2D → 'L' e 3D com 3 canais → 'RGB').
    """
    if modo:
        return Image.fromarray(arr, mode=modo)
    return Image.fromarray(arr)


def save_image(image: Image.Image, formato: str = "PNG") -> bytes:
    """Serializa uma PIL.Image em bytes (padrão PNG) para o st.download_button."""
    buffer = io.BytesIO()
    image.save(buffer, format=formato)
    return buffer.getvalue()


def save_image_to_disk(image: Image.Image, caminho: str) -> str:
    """Salva a imagem em disco. Adiciona .png ao caminho se necessário."""
    if not caminho.lower().endswith(".png"):
        caminho += ".png"
    image.save(caminho, format="PNG")
    return caminho


def save_multiple_images(imagens: dict, prefixo: str = "canal") -> dict:
    """
    Recebe {nome_canal: PIL.Image} e devolve {nome_canal: bytes_png}.
    Útil para as decomposições RGB/HSV que geram 3 imagens de saída.
    """
    return {nome: save_image(img) for nome, img in imagens.items()}