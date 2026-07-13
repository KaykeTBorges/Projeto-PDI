import cv2
import numpy as np

# Aqui implementaremos todos os filtros e transformações
# Exemplo inicial:
def rgb_decomposition(image: np.ndarray):
    """Decompõe a imagem em canais R, G e B"""
    b, g, r = cv2.split(image)
    return {"r": r, "g": g, "b": b}
