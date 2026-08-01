"""
Tudo relacionado à barra lateral: seleção do processo (agrupado por
categoria e filtrado pelo tipo de imagem carregada), renderização dos
widgets de parâmetro de cada processo e o botão de aplicar.
"""

import streamlit as st

from processing.color import rgb_decomposition, hsv_decomposition
from processing.grayscale import thresholding, intensity_transform, histogram_eq
from processing.spatial import smoothing, sharpening, edge_detection, noise, adaptive_median
from processing.frequency import gaussian_filters, butterworth_filters


# ---------------------------------------------------------------------------
# Funções de execução dos processos. A utilização de funções separadas
# permite a passagem de parâmetros específicos para cada processo,
# mantendo o código organizado e modular.
# ---------------------------------------------------------------------------

def run_rgb_decomposition(img, p):
    return rgb_decomposition.decompose_rgb(img)

def run_hsv_decomposition(img, p):
    return hsv_decomposition.decompose_hsv(img)

def run_threshold(img, p):
    return thresholding.threshold(img, p["k"])

def run_log_transform(img, p):
    return intensity_transform.log_transform(img, p["c"])

def run_power_transform(img, p):
    return intensity_transform.power_transform(img, p["c"], p["gamma"])

def run_intensity_slicing(img, p):
    return intensity_transform.intensity_slicing(img, p["a"], p["b"], p["preserve_bg"])

def run_equalize_histogram(img, p):
    return histogram_eq.equalize_histogram(img)

def run_gaussian_mean(img, p):
    return smoothing.gaussian_mean(img, p["sigma"], p["ksize"])

def run_median_filter(img, p):
    return smoothing.median_filter(img, p["ksize"])

def run_min_filter(img, p):
    return smoothing.min_filter(img, p["ksize"])

def run_max_filter(img, p):
    return smoothing.max_filter(img, p["ksize"])

def run_sharpen(img, p):
    return sharpening.sharpen(img, p["gain"], p["ksize"])

def run_laplacian(img, p):
    return edge_detection.laplacian(img, p["ksize"])

def run_sobel(img, p):
    return edge_detection.sobel(img, p["ksize"])

def run_gaussian_noise(img, p):
    return noise.gaussian_noise(img, p["mean"], p["std"])

def run_salt_pepper(img, p):
    return noise.salt_pepper(img, p["amount"], p["salt_vs_pepper"])

def run_adaptive_median(img, p):
    return adaptive_median.adaptive_median(img, p["max_window"])

def run_gaussian_lowpass(img, p):
    return gaussian_filters.gaussian_lowpass(img, p["cutoff"])

def run_gaussian_highpass(img, p):
    return gaussian_filters.gaussian_highpass(img, p["cutoff"])

def run_butterworth_lowpass(img, p):
    return butterworth_filters.butterworth_lowpass(img, p["cutoff"], p["order"])

def run_butterworth_highpass(img, p):
    return butterworth_filters.butterworth_highpass(img, p["cutoff"], p["order"])


# Dicionário de processos disponíveis, com suas categorias, tipos de imagem compatíveis, parâmetros e funções de execução.

PROCESSOS = {
    "Decomposição em RGB": {
        "categoria": "Espaço de cor",
        "tipos": ["rgb"],
        "params": [],
        "acessorio": "decomposicao",
        "fn": run_rgb_decomposition,
    },
    "Decomposição em HSV": {
        "categoria": "Espaço de cor",
        "tipos": ["rgb"],
        "params": [],
        "acessorio": "decomposicao",
        "fn": run_hsv_decomposition,
    },
    "Limiarização": {
        "categoria": "Transformação de intensidade",
        "tipos": ["grayscale"],
        "params": [{"nome": "k", "label": "Limiar (k)", "tipo": "slider", "min": 0, "max": 255, "default": 128}],
        "acessorio": None,
        "fn": run_threshold,
    },
    "Transformação de intensidade logarítmica": {
        "categoria": "Transformação de intensidade",
        "tipos": ["grayscale"],
        "params": [{"nome": "c", "label": "Ganho (c)", "tipo": "number", "min": 0.0, "max": 100.0, "default": 1.0}],
        "acessorio": None,
        "fn": run_log_transform,
    },
    "Transformação de intensidade de potência": {
        "categoria": "Transformação de intensidade",
        "tipos": ["grayscale"],
        "params": [
            {"nome": "c", "label": "Ganho (c)", "tipo": "number", "min": 0.0, "max": 100.0, "default": 1.0},
            {"nome": "gamma", "label": "Gama (γ)", "tipo": "number", "min": 0.01, "max": 25.0, "default": 1.0},
        ],
        "acessorio": None,
        "fn": run_power_transform,
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
        "fn": run_intensity_slicing,
    },
    "Equalização de histograma": {
        "categoria": "Transformação de intensidade",
        "tipos": ["grayscale"],
        "params": [],
        "acessorio": "histogramas",
        "fn": run_equalize_histogram,
    },
    "Filtro de média gaussiana": {
        "categoria": "Filtros espaciais",
        "tipos": ["grayscale", "rgb"],
        "params": [
            {"nome": "sigma", "label": "Desvio padrão (σ)", "tipo": "number", "min": 0.1, "max": 20.0, "default": 1.0},
            {"nome": "ksize", "label": "Tamanho da janela", "tipo": "slider_odd", "min": 3, "max": 21, "default": 5},
        ],
        "acessorio": None,
        "fn": run_gaussian_mean,
    },
    "Filtro de mediana": {
        "categoria": "Filtros espaciais",
        "tipos": ["grayscale", "rgb"],
        "params": [{"nome": "ksize", "label": "Tamanho da janela", "tipo": "slider_odd", "min": 3, "max": 21, "default": 3}],
        "acessorio": None,
        "fn": run_median_filter,
    },
    "Filtro mínimo": {
        "categoria": "Filtros espaciais",
        "tipos": ["grayscale", "rgb"],
        "params": [{"nome": "ksize", "label": "Tamanho da janela", "tipo": "slider_odd", "min": 3, "max": 21, "default": 3}],
        "acessorio": None,
        "fn": run_min_filter,
    },
    "Filtro máximo": {
        "categoria": "Filtros espaciais",
        "tipos": ["grayscale", "rgb"],
        "params": [{"nome": "ksize", "label": "Tamanho da janela", "tipo": "slider_odd", "min": 3, "max": 21, "default": 3}],
        "acessorio": None,
        "fn": run_max_filter,
    },
    "Máscara de aguçamento": {
        "categoria": "Filtros espaciais",
        "tipos": ["grayscale", "rgb"],
        "params": [
            {"nome": "gain", "label": "Ganho do aguçamento", "tipo": "number", "min": 0.0, "max": 10.0, "default": 1.0},
            {"nome": "ksize", "label": "Tamanho da janela", "tipo": "slider_odd", "min": 3, "max": 21, "default": 3},
        ],
        "acessorio": None,
        "fn": run_sharpen,
    },
    "Realce por Laplaciano": {
        "categoria": "Filtros espaciais",
        "tipos": ["grayscale"],
        "params": [{"nome": "ksize", "label": "Tamanho da janela", "tipo": "slider_odd", "min": 3, "max": 21, "default": 3}],
        "acessorio": "laplaciano",
        "fn": run_laplacian,
    },
    "Gradiente de Sobel": {
        "categoria": "Filtros espaciais",
        "tipos": ["grayscale"],
        "params": [
            {"nome": "ksize", "label": "Tamanho da janela", "tipo": "slider_odd", "min": 3, "max": 7, "default": 3},
        ],
        "acessorio": None,
        "fn": run_sobel,
    },
    "Ruído aditivo gaussiano": {
        "categoria": "Ruído",
        "tipos": ["grayscale", "rgb"],
        "params": [
            {"nome": "mean", "label": "Média", "tipo": "number", "min": -50.0, "max": 50.0, "default": 0.0},
            {"nome": "std", "label": "Desvio padrão (intensidade)", "tipo": "number", "min": 0.0, "max": 100.0, "default": 15.0},
        ],
        "acessorio": None,
        "fn": run_gaussian_noise,
    },
    "Ruído sal e pimenta": {
        "categoria": "Ruído",
        "tipos": ["grayscale", "rgb"],
        "params": [
            {"nome": "amount", "label": "Quantidade de ruído", "tipo": "number", "min": 0.0, "max": 1.0, "default": 0.05},
            {"nome": "salt_vs_pepper", "label": "Proporção sal/pimenta", "tipo": "number", "min": 0.0, "max": 1.0, "default": 0.5},
        ],
        "acessorio": None,
        "fn": run_salt_pepper,
    },
    "Filtro adaptativo de mediana": {
        "categoria": "Filtros espaciais",
        "tipos": ["grayscale"],
        "params": [{"nome": "max_window", "label": "Tamanho máximo da janela", "tipo": "slider_odd", "min": 3, "max": 31, "default": 7}],
        "acessorio": None,
        "fn": run_adaptive_median,
    },
    "Filtro passa-baixa gaussiano": {
        "categoria": "Filtros de frequência",
        "tipos": ["grayscale"],
        "params": [{"nome": "cutoff", "label": "Frequência de corte", "tipo": "number", "min": 1.0, "max": 200.0, "default": 30.0}],
        "acessorio": None,
        "fn": run_gaussian_lowpass,
    },
        "Filtro passa-alta gaussiano": {
        "categoria": "Filtros de frequência",
        "tipos": ["grayscale"],
        "params": [{"nome": "cutoff", "label": "Frequência de corte", "tipo": "number", "min": 1.0, "max": 200.0, "default": 30.0}],
        "acessorio": None,
        "fn": run_gaussian_highpass,
    },
    "Filtro passa-baixa Butterworth": {
        "categoria": "Filtros de frequência",
        "tipos": ["grayscale"],
        "params": [
            {"nome": "cutoff", "label": "Frequência de corte", "tipo": "number", "min": 1.0, "max": 200.0, "default": 30.0},
            {"nome": "order", "label": "Ordem do filtro", "tipo": "slider", "min": 1, "max": 10, "default": 2},
        ],
        "acessorio": None,
        "fn": run_butterworth_lowpass,
    },
    "Filtro passa-alta Butterworth": {
        "categoria": "Filtros de frequência",
        "tipos": ["grayscale"],
        "params": [
            {"nome": "cutoff", "label": "Frequência de corte", "tipo": "number", "min": 1.0, "max": 200.0, "default": 30.0},
            {"nome": "order", "label": "Ordem do filtro", "tipo": "slider", "min": 1, "max": 10, "default": 2},
        ],
        "acessorio": None,
        "fn": run_butterworth_highpass,
    },
}

# Ordem fixa de exibição das categorias na sidebar.
ORDEM_CATEGORIAS = [
    "Espaço de cor",
    "Transformação de intensidade",
    "Filtros espaciais",
    "Ruído",
    "Filtros de frequência",
]

def render_sidebar(tipo_imagem: str, info: dict):
    """
    Renderiza a barra lateral: informações da imagem carregada, seletor de
    processo (agrupado por categoria e filtrado por compatibilidade com o
    tipo de imagem) e o botão de aplicar.

    Parâmetros:
    tipo_imagem : str  -> 'grayscale' ou 'rgb', conforme detectado na imagem carregada.
    info        : dict -> informações descritivas da imagem (dimensões, modo, etc.).

    Retorna:
    (processo_nome, aplicar) -> nome do processo selecionado (ou None) e
                                 booleano indicando se o botão foi clicado.
    """
    with st.sidebar:
        st.header("Imagem carregada")
        for chave, valor in info.items():
            st.caption(f"{chave}: {valor}")
        st.caption(f"Tipo detectado: {'Escala de cinza' if tipo_imagem == 'grayscale' else 'Colorida (RGB)'}")

        st.divider()
        st.header("Processo")

        # Filtra as categorias e processos disponíveis com base no tipo de imagem carregada.
        categorias_presentes = [
            categoria for categoria in ORDEM_CATEGORIAS
            if any(infos["categoria"] == categoria for infos in PROCESSOS.values())
            and not (tipo_imagem == "grayscale" and categoria == "Espaço de cor")
        ]

        categoria_selecionada = st.selectbox("Categoria", categorias_presentes)

        opcoes_processo = [
            nome for nome, infos in PROCESSOS.items()
            if infos["categoria"] == categoria_selecionada
        ]

        processo_nome = st.selectbox("Processo", opcoes_processo)

        infos_processo = PROCESSOS[processo_nome]
        if tipo_imagem not in infos_processo["tipos"]:
            st.warning("⚠️ A imagem será convertida para escala de cinza antes de aplicar este processo.")

        aplicar = st.button("Aplicar processo", type="primary", width="stretch")

        return processo_nome, aplicar


def renderizar_parametro(processo_nome: str, param: dict):
    """
    Renderiza o widget correspondente a um único parâmetro de um processo,
    na área principal (chamado por ui.display.render_parametros).

    Tipos de widget suportados:
    - 'slider'     : slider numérico (inteiro) entre min e max.
    - 'slider_odd' : slider numérico (inteiro, apenas ímpares) entre min e max.
    - 'number'     : campo numérico livre (float) entre min e max.
    - 'checkbox'   : caixa de seleção booleana.
    """
    chave = f"{processo_nome}__{param['nome']}"
    tipo = param["tipo"]

    if tipo == "slider":
        return st.slider(
            param["label"],
            min_value=param["min"],
            max_value=param["max"],
            value=param["default"],
            key=chave,
        )

    if tipo == "slider_odd":
        valor = st.slider(
            param["label"],
            min_value=param["min"],
            max_value=param["max"],
            value=param["default"],
            step=2,
            key=chave,
        )
        # Garante que o valor final seja sempre ímpar, mesmo que o usuário
        # tenha chegado nele por outro meio (ex.: teclado).
        if valor % 2 == 0:
            valor += 1
        return valor

    if tipo == "number":
        return st.number_input(
            param["label"],
            min_value=param["min"],
            max_value=param["max"],
            value=param["default"],
            key=chave,
        )

    if tipo == "checkbox":
        return st.checkbox(
            param["label"],
            value=param["default"],
            key=chave,
        )

    raise ValueError(f"Tipo de parâmetro desconhecido: {tipo!r}")
