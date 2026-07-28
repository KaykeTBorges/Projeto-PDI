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

    # Area principal: upload de arquivo, imagens de entrada/saída, parâmetros do processo, resultado (histogramas, laplaciano, decomposições) e botão de download.
    arquivo = display.render_upload_section()
    if arquivo is None:
        st.info("Carregue uma imagem .png para começar.")
        return

    imagem_original = image_io.load_image(arquivo)
    imagem_original = validation.normalize_image(imagem_original)
    tipo_imagem = validation.detect_image_type(imagem_original)
    info = validation.image_info(imagem_original)

    # Sidebar: seleção de processo, parâmetros do processo, botão "Aplicar"
    processo_nome, aplicar = sidebar.render_sidebar(tipo_imagem, info)

    # Aréa principal: exibição da imagem de entrada e criação das colunas para a imagem de saída
    col_original, col_saida = display.render_input_image(imagem_original)

    # Renderiza os parâmetros do processo selecionado, na área principal (abaixo das imagens)
    parametros = display.render_parametros(processo_nome)

    # Guarda o último processo/parâmetros aplicados em session_state, para o
    # resultado continuar visível mesmo após reruns do Streamlit (que
    # acontecem a cada interação com qualquer widget da página).
    if aplicar:
        st.session_state["processo_aplicado"] = processo_nome
        st.session_state["parametros_aplicados"] = parametros

    processo_aplicado = st.session_state.get("processo_aplicado")
    parametros_aplicados = st.session_state.get("parametros_aplicados", {})

    # Executa o processo selecionado (se houver) 
    resultado = None
    extra = None
    if processo_aplicado:
        try:
            saida = sidebar.PROCESSOS[processo_aplicado]["fn"](imagem_original, parametros_aplicados)
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

    # Renderiza a imagem de saída (ou uma mensagem, se o resultado estiver em 'extra'), os acessórios (histogramas, laplaciano, decomposições) e o botão de download do(s) resultado(s).
    display.render_output_image(col_saida, resultado, extra)
    display.render_extra(extra)
    display.render_download_button(resultado)

# Executa a função main() apenas se este arquivo for executado diretamente (não importado como módulo).
if __name__ == "__main__":
    main()