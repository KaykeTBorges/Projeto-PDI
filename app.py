"""
Ponto de entrada do software de Processamento Digital de Imagens (PDI).
Orquestração corrigida com proteção de estado para evitar quebras de cache.
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
        # CORREÇÃO: Limpa o estado se o usuário remover o arquivo para não quebrar o cache
        st.session_state.pop("processo_aplicado", None)
        st.session_state.pop("parametros_aplicados", None)
        st.session_state.pop("processo_atual_interface", None)
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

    # CORREÇÃO: Alinhado com a chave do dicionário de PROCESSOS que usa 'tipos' em vez de 'modo_entrada'
    processo_infos = sidebar.PROCESSOS.get(processo_nome, {})
    requer_gray_selecionado = (
        processo_nome is not None
        and "grayscale" in processo_infos.get("tipos", [])
        and "rgb" not in processo_infos.get("tipos", [])
        and imagem_original.mode != "L"
    )
    imagem_exibida = imagem_original.convert("L") if requer_gray_selecionado else imagem_original

    col_original, col_saida = display.render_input_image(imagem_exibida)
    if requer_gray_selecionado:
        with col_original:
            st.caption("Exibida em grayscale — o processo selecionado requer esse modo.")

    parametros = display.render_parametros(processo_nome)

    # CORREÇÃO: Se o usuário mudou o processo selecionado na barra lateral,
    # nós limpamos o resultado anterior para evitar conflitos de parâmetros antigos com o filtro novo.
    if st.session_state.get("processo_atual_interface") != processo_nome:
        st.session_state["processo_atual_interface"] = processo_nome
        st.session_state.pop("processo_aplicado", None)
        st.session_state.pop("parametros_aplicados", None)

    # Se clicou em aplicar, aí sim fixamos a execução no estado
    if aplicar:
        st.session_state["processo_aplicado"] = processo_nome
        st.session_state["parametros_aplicados"] = parametros

    processo_aplicado = st.session_state.get("processo_aplicado")
    parametros_aplicados = st.session_state.get("parametros_aplicados", {})

    resultado = None
    extra = None
    
    if processo_aplicado:
        processo_aplicado_infos = sidebar.PROCESSOS.get(processo_aplicado, {})
        # CORREÇÃO: Ajuste fino na detecção se o filtro aplicado exige tons de cinza
        deve_converter = (
            "grayscale" in processo_aplicado_infos.get("tipos", []) 
            and "rgb" not in processo_aplicado_infos.get("tipos", [])
            and imagem_original.mode != "L"
        )
        imagem_para_processar = imagem_original.convert("L") if deve_converter else imagem_original
        
        # MELHORIA DE UX: mostra um spinner enquanto o processo roda, já que
        # alguns filtros (ex: Filtro adaptativo de mediana) podem demorar
        # vários segundos em imagens grandes.
        try:
            with st.spinner(f"Aplicando '{processo_aplicado}'... isso pode levar alguns segundos."):
                saida = sidebar.PROCESSOS[processo_aplicado]["fn"](imagem_para_processar, parametros_aplicados)
        except Exception as e:
            st.error(f"Erro ao executar o processo '{processo_aplicado}': {e}")
            saida = None

        acessorio = sidebar.PROCESSOS[processo_aplicado]["acessorio"]
        
        # CORREÇÃO CRÍTICA: Desempacotamento seguro baseado no tipo de acessório e tamanho do retorno.
        # Evita o erro 'too many values to unpack' checando se a tupla tem o tamanho esperado.
        if saida is not None:
            if acessorio == "decomposicao":
                resultado = None
                extra = saida
                
            elif acessorio == "histogramas":
                if isinstance(saida, tuple) and len(saida) == 3:
                    resultado, hist_antes, hist_depois = saida
                    extra = {"hist_antes": hist_antes, "hist_depois": hist_depois}
                else:
                    resultado = saida
                    extra = None
                    
            elif acessorio == "laplaciano":
                if isinstance(saida, tuple) and len(saida) == 2:
                    resultado, laplaciano = saida
                    extra = {"laplaciano": laplaciano}
                else:
                    # Se houver lixo residual no cache que retorne 3 elementos, extrai o primeiro com segurança
                    resultado = saida[0] if isinstance(saida, (tuple, list)) else saida
                    extra = None
            else:
                # Filtros comuns de imagem única (como o Filtro Adaptativo de Mediana) caem aqui
                resultado = saida[0] if isinstance(saida, (tuple, list)) else saida
                extra = None

    display.render_output_image(col_saida, resultado, extra)
    display.render_extra(extra)
    display.render_download_button(resultado)


if __name__ == "__main__":
    main()