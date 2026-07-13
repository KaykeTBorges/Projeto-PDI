import cv2
import numpy as np
import base64

def decode_image(file_bytes: bytes) -> tuple[np.ndarray, bool]:
    """
    Decodifica os bytes recebidos via HTTP para uma matriz NumPy (imagem).
    Retorna a imagem e um booleano (is_color) indicando se ela é colorida.
    """
    # Converte os bytes puros em um array do NumPy
    nparr = np.frombuffer(file_bytes, np.uint8)
    
    # Decodifica usando o OpenCV preservando os canais exatos do arquivo original
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    
    if img is None:
        raise ValueError("Falha ao decodificar a imagem. O arquivo pode estar corrompido.")

    # Verifica se a imagem é Tons de Cinza (Matriz 2D) ou Colorida (Matriz 3D)
    if len(img.shape) == 2:
        return img, False  # É Tons de Cinza
    
    elif len(img.shape) == 3:
        canais = img.shape[2]
        if canais == 3:
            # Imagem Colorida Padrão. O OpenCV lê como BGR, nós convertemos para RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img_rgb, True
        elif canais == 4:
            # Imagem com Transparência (BGRA). Convertemos para RGB e descartamos o Alpha
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
            return img_rgb, True
            
    raise ValueError("Formato de imagem não suportado. Use imagens de 8-bits ou 24-bits.")

def encode_image(img: np.ndarray, is_color: bool) -> bytes:
    """
    Pega uma matriz matemática (imagem) e transforma de volta em bytes de arquivo PNG.
    Se ela for colorida (RGB), reverte para BGR pro OpenCV salvar com as cores certas.
    """
    # Usamos uma cópia para não poluir a matriz que pode estar sendo usada por outro processo
    img_to_encode = img.copy()
    
    # Se a matriz de entrada for classificada como colorida e tiver 3 dimensões
    if is_color and len(img_to_encode.shape) == 3 and img_to_encode.shape[2] == 3:
        # OpenCV exige BGR para salvar
        img_to_encode = cv2.cvtColor(img_to_encode, cv2.COLOR_RGB2BGR)
            
    # Converte a matriz de volta para o formato de arquivo .png em memória
    success, encoded_img = cv2.imencode('.png', img_to_encode)
    
    if not success:
        raise ValueError("Falha ao codificar a imagem resultante para PNG.")
        
    return encoded_img.tobytes()

def encode_image_base64(img: np.ndarray, is_color: bool) -> str:
    """
    Codifica a imagem em formato Base64.
    Extremamente útil para enviar múltiplas imagens dentro de um único pacote JSON
    (como exigido pela Decomposição RGB/HSV ou envio de Gráficos de Histograma).
    """
    img_bytes = encode_image(img, is_color)
    return base64.b64encode(img_bytes).decode('utf-8')
