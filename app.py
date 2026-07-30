""""
Ponto de entrada do software de Processamento Digital de Imagens (PDI).

Este arquivo só orquestra: carrega a imagem, chama a sidebar (ui/sidebar.py)
para obter o processo escolhido, chama a área principal (ui/display.py)
para exibir upload/imagens/parâmetros/resultado, executa a função de
processamento e guarda o estado em st.session_state.
"""

import streamlit as st
from PIL import Image

from utils import image_io
from utils import validation
from ui import sidebar
from ui import display


st.set_page_config(page_title="PDI - Processamento Digital de Imagens", layout="wide")


def main():
    st.title("Software de Processamento Digital de Imagens")
    st.caption("Feito para a disciplina de Introdução ao Processamento Digital de Imagens")

    arquivo = display.render_upload_section()
    if arquivo is None:
        st.info("Carregue uma imagem .png para começar.")
        return

    imagem_original = image_io.load_image(arquivo)
    modo_antes = imagem_original.mode
    imagem_original = validation.normalize_image(imagem_original)
    if modo_antes == "RGB" and imagem_original.mode == "L":
        st.info("Imagem detectada como grayscale (estava salva em modo RGB) — convertida automaticamente.")
    tipo_imagem = validation.detect_image_type(imagem_original)
    info = validation.image_info(imagem_original)

    processo_nome, aplicar = sidebar.render_sidebar(tipo_imagem, info)

    # Se o processo selecionado requer grayscale e a imagem é RGB,
    # exibe a versão convertida como "entrada" para o usuário.
    requer_gray_selecionado = (
        processo_nome is not None
        and sidebar.PROCESSOS.get(processo_nome, {}).get("modo_entrada") == "grayscale"
        and imagem_original.mode != "L"
    )
    imagem_exibida = imagem_original.convert("L") if requer_gray_selecionado else imagem_original

    col_original, col_saida = display.render_input_image(imagem_exibida)
    if requer_gray_selecionado:
        with col_original:
            st.caption("Exibida em grayscale — o processo selecionado requer esse modo.")

    parametros = display.render_parametros(processo_nome)

    # Guarda o último processo/parâmetros aplicados em session_state, para o
    # resultado continuar visível mesmo após reruns do Streamlit (que
    # acontecem a cada interação com qualquer widget da página).
    if aplicar:
        st.session_state["processo_aplicado"] = processo_nome
        st.session_state["parametros_aplicados"] = parametros

    processo_aplicado = st.session_state.get("processo_aplicado")
    parametros_aplicados = st.session_state.get("parametros_aplicados", {})

    resultado = None
    extra = None
    if processo_aplicado:
        modo_entrada = sidebar.PROCESSOS.get(processo_aplicado, {}).get("modo_entrada")
        imagem_para_processar = (
            imagem_original.convert("L")
            if modo_entrada == "grayscale" and imagem_original.mode != "L"
            else imagem_original
        )
        try:
            saida = sidebar.PROCESSOS[processo_aplicado]["fn"](imagem_para_processar, parametros_aplicados)
        except Exception as e:
            st.error(f"Erro ao executar o processo '{processo_aplicado}': {e}")
            saida = None

        acessorio = sidebar.PROCESSOS[processo_aplicado]["acessorio"]
        if acessorio == "decomposicao" and saida is not None:
            resultado = None
            extra = saida
        elif acessorio == "histogramas" and saida is not None:
            resultado, hist_antes, hist_depois = saida
            extra = {"hist_antes": hist_antes, "hist_depois": hist_depois}
        elif acessorio == "laplaciano" and saida is not None:
            resultado, laplaciano = saida
            extra = {"laplaciano": laplaciano}
        else:
            resultado = saida

    display.render_output_image(col_saida, resultado, extra)
    display.render_extra(extra)
    display.render_download_button(resultado)

if __name__ == "__main__":
    main()