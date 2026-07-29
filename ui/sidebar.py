"""
Tudo relacionado à barra lateral: o catálogo de processos disponíveis
(PROCESSOS), a renderização dos widgets de parâmetro, e a seção de
"Seleção de processos" (categoria, processo, botão Aplicar).
"""

import streamlit as st

from processing.color import rgb_decomposition
from processing.color import hsv_decomposition

from processing.grayscale import thresholding
from processing.grayscale import intensity_transform
from processing.grayscale import histogram_eq

from processing.spatial import smoothing
from processing.spatial import sharpening
from processing.spatial import edge_detection
from processing.spatial import noise
from processing.spatial import adaptive_median

from processing.frequency import gaussian_filters
from processing.frequency import butterworth_filters


# ---------------------------------------------------------------------------
# Definição dos processos disponíveis, organizados por categoria.
# "tipos": para quais tipos de imagem o processo é habilitado
#   ("grayscale", "rgb" ou ambos)
# "acessorio": indica se o processo retorna dado(s) extra(s) além da imagem
#   de saída (histogramas, laplaciano, decomposições em canais).
# ---------------------------------------------------------------------------
PROCESSOS = {
    "Decomposição em componentes RGB": {
        "categoria": "Espaço de cor",
        "tipos": ["rgb"],
        "params": [],
        "acessorio": "decomposicao",
        "fn": lambda img, p: rgb_decomposition.decompose_rgb(img),
    },
    "Decomposição em componentes HSV": {
        "categoria": "Espaço de cor",
        "tipos": ["rgb"],
        "params": [],
        "acessorio": "decomposicao",
        "fn": lambda img, p: hsv_decomposition.decompose_hsv(img),
    },
    "Limiarização": {
        "categoria": "Transformação de intensidade",
        "tipos": ["grayscale"],
        "params": [{"nome": "k", "label": "Limiar (k)", "tipo": "slider", "min": 0, "max": 255, "default": 128}],
        "acessorio": None,
        "fn": lambda img, p: thresholding.threshold(img, p["k"]),
    },
    "Transformação de intensidade logarítmica": {
        "categoria": "Transformação de intensidade",
        "tipos": ["grayscale"],
        "params": [{"nome": "c", "label": "Ganho (c)", "tipo": "number", "min": 0.0, "max": 100.0, "default": 1.0}],
        "acessorio": None,
        "fn": lambda img, p: intensity_transform.log_transform(img, p["c"]),
    },
    "Transformação de intensidade de potência": {
        "categoria": "Transformação de intensidade",
        "tipos": ["grayscale"],
        "params": [
            {"nome": "c", "label": "Ganho (c)", "tipo": "number", "min": 0.0, "max": 100.0, "default": 1.0},
            {"nome": "gamma", "label": "Gama (γ)", "tipo": "number", "min": 0.01, "max": 25.0, "default": 1.0},
        ],
        "acessorio": None,
        "fn": lambda img, p: intensity_transform.power_transform(img, p["c"], p["gamma"]),
    },
    "Fatiamento por intensidade": {
        "categoria": "Transformação de intensidade",
        "tipos": ["grayscale"],
        "params": [
            {"nome": "a", "label": "Faixa mínima (A)", "tipo": "slider", "min": 0, "max": 255, "default": 80},
            {"nome": "b", "label": "Faixa máxima (B)", "tipo": "slider", "min": 0, "max": 255, "default": 180},
            {"nome": "preserve_bg", "label": "Preservar fundo", "tipo": "checkbox", "default": True},
        ],
        "acessorio": None,
        "fn": lambda img, p: intensity_transform.intensity_slicing(img, p["a"], p["b"], p["preserve_bg"]),
    },
    "Equalização de histograma": {
        "categoria": "Transformação de intensidade",
        "tipos": ["grayscale"],
        "params": [],
        "acessorio": "histogramas",
        "fn": lambda img, p: histogram_eq.equalize_histogram(img),
    },
    "Filtro de média gaussiana": {
        "categoria": "Filtros espaciais",
        "tipos": ["grayscale", "rgb"],
        "params": [
            {"nome": "sigma", "label": "Desvio padrão (σ)", "tipo": "number", "min": 0.1, "max": 20.0, "default": 1.0},
            {"nome": "ksize", "label": "Tamanho da janela", "tipo": "slider_odd", "min": 3, "max": 21, "default": 5},
        ],
        "acessorio": None,
        "fn": lambda img, p: smoothing.gaussian_mean(img, p["sigma"], p["ksize"]),
    },
    "Filtro de mediana": {
        "categoria": "Filtros espaciais",
        "tipos": ["grayscale", "rgb"],
        "params": [{"nome": "ksize", "label": "Tamanho da janela", "tipo": "slider_odd", "min": 3, "max": 21, "default": 3}],
        "acessorio": None,
        "fn": lambda img, p: smoothing.median_filter(img, p["ksize"]),
    },
    "Filtro mínimo": {
        "categoria": "Filtros espaciais",
        "tipos": ["grayscale", "rgb"],
        "params": [{"nome": "ksize", "label": "Tamanho da janela", "tipo": "slider_odd", "min": 3, "max": 21, "default": 3}],
        "acessorio": None,
        "fn": lambda img, p: smoothing.min_filter(img, p["ksize"]),
    },
    "Filtro máximo": {
        "categoria": "Filtros espaciais",
        "tipos": ["grayscale", "rgb"],
        "params": [{"nome": "ksize", "label": "Tamanho da janela", "tipo": "slider_odd", "min": 3, "max": 21, "default": 3}],
        "acessorio": None,
        "fn": lambda img, p: smoothing.max_filter(img, p["ksize"]),
    },
    "Máscara de aguçamento": {
        "categoria": "Filtros espaciais",
        "tipos": ["grayscale", "rgb"],
        "params": [
            {"nome": "gain", "label": "Ganho do aguçamento", "tipo": "number", "min": 0.0, "max": 10.0, "default": 1.0},
            {"nome": "ksize", "label": "Tamanho da janela", "tipo": "slider_odd", "min": 3, "max": 21, "default": 3},
        ],
        "acessorio": None,
        "fn": lambda img, p: sharpening.sharpen(img, p["gain"], p["ksize"]),
    },
    "Realce por Laplaciano": {
        "categoria": "Filtros espaciais",
        "tipos": ["grayscale"],
        "params": [{"nome": "ksize", "label": "Tamanho da janela", "tipo": "slider_odd", "min": 3, "max": 21, "default": 3}],
        "acessorio": "laplaciano",
        "fn": lambda img, p: edge_detection.laplacian(img, p["ksize"]),
    },
    "Gradiente de Sobel": {
        "categoria": "Filtros espaciais",
        "tipos": ["grayscale"],
        "params": [{"nome": "ksize", "label": "Tamanho da janela", "tipo": "slider_odd", "min": 3, "max": 21, "default": 3}],
        "acessorio": None,
        "fn": lambda img, p: edge_detection.sobel(img, p["ksize"]),
    },
    "Ruído aditivo gaussiano": {
        "categoria": "Ruído",
        "tipos": ["grayscale", "rgb"],
        "params": [
            {"nome": "mean", "label": "Média", "tipo": "number", "min": -50.0, "max": 50.0, "default": 0.0},
            {"nome": "std", "label": "Desvio padrão (intensidade)", "tipo": "number", "min": 0.0, "max": 100.0, "default": 15.0},
        ],
        "acessorio": None,
        "fn": lambda img, p: noise.gaussian_noise(img, p["mean"], p["std"]),
    },
    "Ruído sal e pimenta": {
        "categoria": "Ruído",
        "tipos": ["grayscale", "rgb"],
        "params": [
            {"nome": "amount", "label": "Quantidade de ruído", "tipo": "number", "min": 0.0, "max": 1.0, "default": 0.05},
            {"nome": "salt_vs_pepper", "label": "Proporção sal/pimenta", "tipo": "number", "min": 0.0, "max": 1.0, "default": 0.5},
        ],
        "acessorio": None,
        "fn": lambda img, p: noise.salt_pepper(img, p["amount"], p["salt_vs_pepper"]),
    },
    "Filtro adaptativo de mediana": {
        "categoria": "Filtros de frequência",
        "tipos": ["grayscale"],
        "params": [{"nome": "max_window", "label": "Tamanho máximo da janela", "tipo": "slider_odd", "min": 3, "max": 31, "default": 7}],
        "acessorio": None,
        "fn": lambda img, p: adaptive_median.adaptive_median(img, p["max_window"]),
    },
    "Filtro passa-baixa gaussiano": {
        "categoria": "Filtros de frequência",
        "tipos": ["grayscale"],
        "params": [{"nome": "cutoff", "label": "Frequência de corte", "tipo": "number", "min": 1.0, "max": 200.0, "default": 30.0}],
        "acessorio": None,
        "fn": lambda img, p: gaussian_filters.gaussian_lowpass(img, p["cutoff"]),
    },
    "Filtro passa-alta gaussiano": {
        "categoria": "Filtros de frequência",
        "tipos": ["grayscale"],
        "params": [{"nome": "cutoff", "label": "Frequência de corte", "tipo": "number", "min": 1.0, "max": 200.0, "default": 30.0}],
        "acessorio": None,
        "fn": lambda img, p: gaussian_filters.gaussian_highpass(img, p["cutoff"]),
    },
    "Filtro passa-baixa de Butterworth": {
        "categoria": "Filtros de frequência",
        "tipos": ["grayscale"],
        "params": [
            {"nome": "cutoff", "label": "Frequência de corte", "tipo": "number", "min": 1.0, "max": 200.0, "default": 30.0},
            {"nome": "order", "label": "Ordem", "tipo": "slider", "min": 1, "max": 10, "default": 2},
        ],
        "acessorio": None,
        "fn": lambda img, p: butterworth_filters.butterworth_lowpass(img, p["cutoff"], p["order"]),
    },
    "Filtro passa-alta de Butterworth": {
        "categoria": "Filtros de frequência",
        "tipos": ["grayscale"],
        "params": [
            {"nome": "cutoff", "label": "Frequência de corte", "tipo": "number", "min": 1.0, "max": 200.0, "default": 30.0},
            {"nome": "order", "label": "Ordem", "tipo": "slider", "min": 1, "max": 10, "default": 2},
        ],
        "acessorio": None,
        "fn": lambda img, p: butterworth_filters.butterworth_highpass(img, p["cutoff"], p["order"]),
    },
}

# Processos que só funcionam internamente com imagem grayscale passam a
# aceitar RGB também — a conversão é feita pelo app.py antes de chamar a função.
for _proc in PROCESSOS.values():
    if _proc["tipos"] == ["grayscale"]:
        _proc["tipos"] = ["grayscale", "rgb"]
        _proc["modo_entrada"] = "grayscale"


def renderizar_parametro(processo_nome: str, param: dict):
    """Renderiza o widget de parâmetro adequado e retorna o valor escolhido."""
    key = f"{processo_nome}_{param['nome']}"
    tipo = param["tipo"]

    if tipo == "slider":
        return st.slider(param["label"], min_value=param["min"], max_value=param["max"], value=param["default"], key=key)
    if tipo == "slider_odd":
        valor = st.slider(param["label"], min_value=param["min"], max_value=param["max"], value=param["default"], step=2, key=key)
        return valor if valor % 2 == 1 else valor + 1
    if tipo == "number":
        return st.number_input(param["label"], min_value=param["min"], max_value=param["max"], value=param["default"], key=key)
    if tipo == "checkbox":
        return st.checkbox(param["label"], value=param["default"], key=key)
    raise ValueError(f"Tipo de parâmetro desconhecido: {tipo}")


def render_sidebar(tipo_imagem: str, info: dict) -> tuple[str | None, bool]:
    """
    Renderiza a seção "Seleção de processos" na sidebar: informações da
    imagem, escolha de categoria, escolha de processo (com desabilitação
    condicional pelo tipo de imagem) e o botão "Aplicar processo".

    Retorna:
        (processo_nome, aplicar) -> nome do processo selecionado (ou None)
        e um booleano indicando se o botão "Aplicar" foi clicado nesta
        execução do script.
    """
    with st.sidebar:
        st.divider()
        st.header("Seleção de processos")

        st.caption(f"Modo: {info['modo']} | Dimensões: {info['dimensoes']}")
        st.caption(f"Tipo detectado: **{tipo_imagem.upper()}**")

        st.divider()
        categorias = sorted({p["categoria"] for p in PROCESSOS.values()})
        categoria_selecionada = st.selectbox("Categoria", categorias)

        # Processos da categoria, desabilitando os incompatíveis com o tipo de imagem
        nomes_categoria = [n for n, p in PROCESSOS.items() if p["categoria"] == categoria_selecionada]
        opcoes_habilitadas = [n for n in nomes_categoria if tipo_imagem in PROCESSOS[n]["tipos"]]
        opcoes_desabilitadas = [n for n in nomes_categoria if tipo_imagem not in PROCESSOS[n]["tipos"]]

        if not opcoes_habilitadas:
            st.warning("Nenhum processo desta categoria é aplicável ao tipo de imagem carregada.")
            processo_nome = None
        else:
            processo_nome = st.radio("Processo", opcoes_habilitadas)

        if opcoes_desabilitadas:
            st.caption("Desabilitados para este tipo de imagem: " + ", ".join(opcoes_desabilitadas))

        st.divider()
        aplicar = st.button("Aplicar processo", width="stretch", disabled=(processo_nome is None))

    return processo_nome, aplicar