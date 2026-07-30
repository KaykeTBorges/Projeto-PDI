"""
utils/validation.py
--------------------
Funções de validação e detecção do tipo de imagem (grayscale 8-bit vs
RGB 24-bit), usadas pelo app.py para habilitar/desabilitar processos
condicionalmente.
"""

import numpy as np
from PIL import Image


TIPOS_VALIDOS = ("grayscale", "rgb")


def _is_grayscale_rgb(image: Image.Image) -> bool:
    """Verifica se uma imagem em modo RGB é na prática grayscale (R == G == B em todo pixel)."""
    arr = np.asarray(image)
    return np.array_equal(arr[:, :, 0], arr[:, :, 1]) and np.array_equal(arr[:, :, 0], arr[:, :, 2])


def detect_image_type(image: Image.Image) -> str:
    """
    Detecta o tipo da imagem com base no modo do PIL.

    Retorna:
        "grayscale" -> imagem em escala de cinza de 8 bits (modo 'L')
        "rgb"       -> imagem colorida de 24 bits (modo 'RGB'/'RGBA'/'P')

    Qualquer outro modo é tratado como "rgb" após conversão, garantindo
    que o app sempre trabalhe com um dos dois tipos suportados.
    """
    mode = image.mode

    if mode == "L":
        return "grayscale"
    if mode == "RGB":
        return "grayscale" if _is_grayscale_rgb(image) else "rgb"
    if mode in ("RGBA", "P", "CMYK", "YCbCr"):
        return "rgb"

    # Modos incomuns (ex.: '1' bilevel, 'I', 'F') caem aqui.
    # '1' (bilevel/preto e branco puro) é tratado como grayscale.
    if mode == "1":
        return "grayscale"

    return "rgb"


def normalize_image(image: Image.Image) -> Image.Image:
    """
    Normaliza a imagem para um dos dois modos suportados pelo pipeline
    de processamento: 'L' (grayscale 8-bit) ou 'RGB' (24-bit).
    """
    tipo = detect_image_type(image)
    if tipo == "grayscale":
        return image.convert("L")
    return image.convert("RGB")


def image_info(image: Image.Image) -> dict:
    """
    Retorna metadados úteis para exibição na interface (sidebar), como
    modo original, dimensões e o tipo detectado.
    """
    return {
        "modo": image.mode,
        "dimensoes": f"{image.width} x {image.height}",
        "largura": image.width,
        "altura": image.height,
        "tipo_detectado": detect_image_type(image),
    }


def validate_png_upload(arquivo) -> bool:
    """
    Valida se o arquivo enviado pelo st.file_uploader é um .png legível.
    Retorna True/False; não levanta exceção (útil para checagens rápidas
    de UI antes de tentar processar a imagem).
    """
    if arquivo is None:
        return False

    nome = getattr(arquivo, "name", "")
    if nome and not nome.lower().endswith(".png"):
        return False

    try:
        imagem = Image.open(arquivo)
        imagem.verify()  # checa integridade sem carregar os pixels
        arquivo.seek(0)  # reposiciona o buffer para uso posterior (load_image)
        return True
    except Exception:
        return False


def is_process_enabled(tipo_imagem: str, tipos_suportados: list) -> bool:
    """
    Retorna True se o processo (definido pela lista de tipos que ele
    suporta) está habilitado para o tipo de imagem carregado.
    Usado para a habilitação/desabilitação condicional na sidebar.
    """
    return tipo_imagem in tipos_suportados