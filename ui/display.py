"""
Tudo relacionado à área principal da página: upload de arquivo, exibição
lado a lado da imagem de entrada/saída, renderização dos parâmetros do
processo selecionado, exibição de dados/imagens acessórias (histogramas,
laplaciano, decomposições) e os botões de download do(s) resultado(s).
"""

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from PIL import Image

from utils import image_io
from ui.sidebar import PROCESSOS, renderizar_parametro


def render_upload_section():
    """Renderiza a seção de upload de arquivo no topo da área principal."""
    st.header("Opções de arquivo")
    arquivo = st.file_uploader("Carregar imagem (.png)", type=["png"])
    st.divider()
    return arquivo


def render_input_image(imagem_original: Image.Image):
    """
    Renderiza as colunas de imagem de entrada/saída, já exibindo a imagem
    de entrada. Retorna as duas colunas para que a imagem de saída seja
    preenchida depois (assim que o processamento for concluído).
    """
    col_original, col_saida = st.columns(2)
    with col_original:
        st.subheader("Imagem de entrada")
        st.image(imagem_original, width="stretch")
    return col_original, col_saida


def render_parametros(processo_nome: str | None) -> dict:
    """
    Renderiza os widgets de parâmetro do processo selecionado, na área
    principal (abaixo das imagens). Retorna um dicionário {nome: valor}.
    """
    st.divider()
    st.subheader("Parâmetros do processo selecionado")

    parametros = {}
    if processo_nome:
        for param in PROCESSOS[processo_nome]["params"]:
            parametros[param["nome"]] = renderizar_parametro(processo_nome, param)
        if not PROCESSOS[processo_nome]["params"]:
            st.caption("Este processo não possui parâmetros ajustáveis.")
    else:
        st.caption("Selecione um processo na barra lateral.")

    return parametros


def render_output_image(col_saida, resultado, extra):
    """Renderiza a imagem de saída (ou uma mensagem, se o resultado estiver em 'extra')."""
    with col_saida:
        st.subheader("Imagem de saída")
        if resultado is not None:
            st.image(resultado, width="stretch")
        elif extra is not None:
            st.caption("Veja o resultado na seção 'Dados/Imagens acessórias' abaixo.")
        else:
            st.caption("Selecione um processo e clique em 'Aplicar processo'.")


def render_extra(extra: dict | None):
    """
    Renderiza dados/imagens acessórias: histogramas (equalização),
    laplaciano (realce por Laplaciano) ou as 3 imagens de canal
    (decomposição RGB/HSV), cada uma com seu próprio botão de download.
    """
    if not extra:
        return

    st.divider()
    st.subheader("Dados/Imagens acessórias")

    if "hist_antes" in extra:
        c1, c2 = st.columns(2)
        x = np.arange(256)

        with c1:
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.bar(x, extra["hist_antes"], color="#4a90d9", width=1.0)
            ax.set_title("Antes da equalização")
            ax.set_xlabel("Tom de cinza (0–255)")
            ax.set_ylabel("Frequência normalizada")
            ax.set_xlim(0, 255)
            st.pyplot(fig)
            plt.close(fig)

        with c2:
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.bar(x, extra["hist_depois"], color="#e07b39", width=1.0)
            ax.set_title("Depois da equalização")
            ax.set_xlabel("Tom de cinza (0–255)")
            ax.set_ylabel("Frequência normalizada")
            ax.set_xlim(0, 255)
            st.pyplot(fig)
            plt.close(fig)

    if "laplaciano" in extra:
        st.caption("Laplaciano da imagem")
        st.image(extra["laplaciano"], width="stretch")

    # Decomposições RGB/HSV
    eh_decomposicao = (
        isinstance(extra, dict)
        and all(isinstance(v, Image.Image) for v in extra.values())
        and "laplaciano" not in extra
    )
    if eh_decomposicao:
        colunas = st.columns(len(extra))
        for coluna, (nome_canal, img_canal) in zip(colunas, extra.items()):
            with coluna:
                st.caption(f"Canal {nome_canal}")
                st.image(img_canal, width="stretch")
                st.download_button(
                    label=f"Salvar canal {nome_canal}",
                    data=image_io.save_image(img_canal),
                    file_name=f"canal_{nome_canal}.png",
                    mime="image/png",
                    key=f"download_{nome_canal}",
                )


def render_download_button(resultado):
    """Renderiza o botão de download da imagem de saída, quando houver apenas uma."""
    st.divider()
    imagem_para_salvar = resultado if isinstance(resultado, Image.Image) else None
    if imagem_para_salvar is not None:
        st.download_button(
            label="Salvar imagem de saída como .png",
            data=image_io.save_image(imagem_para_salvar),
            file_name="resultado.png",
            mime="image/png",
        )
    else:
        st.caption("O botão de salvar aparece quando o processo selecionado gera uma única imagem de saída.")