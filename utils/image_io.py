"""
Funções de entrada e saída de imagens usadas pela aplicação.

- load_image: recebe o objeto retornado pelo st.file_uploader (ou um
  caminho/arquivo binário) e devolve uma PIL.Image.
- save_image: recebe uma PIL.Image e devolve os bytes prontos para
  download como .png (usado no st.download_button).
"""

import io
from PIL import Image


def load_image(arquivo) -> Image.Image:
    """
    Carrega uma imagem a partir do objeto de upload do Streamlit
    (UploadedFile) ou de um caminho/arquivo binário compatível com PIL.

    Levanta ValueError se o arquivo não puder ser aberto como imagem.
    """
    try:
        imagem = Image.open(arquivo)
        imagem.load()  
        return imagem
    except Exception as e:
        raise ValueError(f"Não foi possível abrir a imagem: {e}")


def save_image(image: Image.Image, formato: str = "PNG") -> bytes:
    """
    Converte uma PIL.Image em bytes no formato solicitado (padrão PNG),
    prontos para serem oferecidos em um st.download_button.
    """
    buffer = io.BytesIO()
    image.save(buffer, format=formato)
    return buffer.getvalue()


def save_image_to_disk(image: Image.Image, caminho: str) -> str:
    """
    Salva a imagem diretamente em disco no caminho informado.
    Útil para testes/scripts fora da interface Streamlit.
    """
    if not caminho.lower().endswith(".png"):
        caminho += ".png"
    image.save(caminho, format="PNG")
    return caminho


def save_multiple_images(imagens: dict, prefixo: str = "canal") -> dict:
    """
    Recebe um dicionário {nome_canal: PIL.Image} — como o retorno das
    decomposições RGB/HSV, que geram 3 imagens de saída — e devolve um
    dicionário {nome_canal: bytes_png}, pronto para múltiplos
    st.download_button na interface.

    Exemplo de uso no app.py:
        bytes_por_canal = image_io.save_multiple_images(extra)
        for canal, dados in bytes_por_canal.items():
            st.download_button(f"Salvar canal {canal}", dados,
                                file_name=f"{prefixo}_{canal}.png")
    """
    resultado = {}
    for nome_canal, imagem in imagens.items():
        resultado[nome_canal] = save_image(imagem)
    return resultado