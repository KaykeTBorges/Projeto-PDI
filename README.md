# Processamento Digital de Imagens (PDI) — UFPB

Projeto desenvolvido para a **Avaliação da 3ª Unidade** da disciplina de **Introdução ao Processamento Digital de Imagens** do Centro de Informática (CI / DSC) — **Universidade Federal da Paraíba (UFPB)**.

**Professor:** Augusto de Holanda B. M. Tavares  
**Tecnologias:** Python, Streamlit, OpenCV, NumPy, Matplotlib, Pillow

---

## Sobre o Projeto

O objetivo deste software é permitir a aplicação interativa de diversas técnicas de **Processamento Digital de Imagens (PDI)** em tempo real, com ajuste dinâmico de parâmetros, extração de métricas e visualização de histogramas.

A aplicação atende a todos os requisitos da disciplina, suportando tanto **imagens em escala de cinza (8 bits)** quanto **imagens coloridas RGB (24 bits)** no formato `.png`.

---

## Funcionalidades Implementadas

O sistema contempla todos os processos exigidos na avaliação:

### Decomposição e Espaços de Cor
* **Decomposição RGB:** Separação da imagem nos canais individuais R, G e B (escala de cinza).
* **Decomposição HSV:** Conversão para o espaço HSV e exibição dos canais H (Matiz), S (Saturação) e V (Valor/Brilho).

### Transformações de Intensidade e Histograma
* **Limiarização (Thresholding):** Binarização com ajuste do valor de limiar $k$.
* **Transformação Logarítmica:** Expansão de tons escuros com ganho $c$ ajustável.
* **Transformação de Potência (Gama):** Ajuste de contraste via lei da potência ($s = c \cdot r^\gamma$).
* **Equalização de Histograma:** Equalização para imagens em escala de cinza com exibição dos histogramas de intensidade antes e depois do processamento.
* **Fatiamento por Intensidade:** Destaque de faixa de interesse $[A, B]$ com opção de preservar ou zerar o fundo.

### Filtragem Espacial e Realce
* **Filtro de Média Gaussiana:** Suavização espacial com ajuste de desvio padrão $\sigma$ e tamanho da janela.
* **Filtros de Ordem (Mediana, Mínimo e Máximo):** Remoção de ruído e ajuste estrutural com janela variável.
* **Máscara de Aguçamento (Unsharp Masking):** Realce de bordas com ajuste do ganho $k$ e janela.
* **Realce por Laplaciano:** Exibição do mapa Laplaciano ajustado e da imagem realçada.
* **Gradiente de Sobel:** Destaque de bordas via magnitude dos operadores Sobel $G_x$ e $G_y$.

### Filtragem no Domínio da Frequência (Fourier)
* **Filtros Gaussianos (Passa-Baixa / Passa-Alta):** Suavização ou aguçamento frequencial sem anelamento, com frequência de corte $D_0$ ajustável.
* **Filtros Butterworth (Passa-Baixa / Passa-Alta):** Controle da transição via frequência de corte $D_0$ e ordem do filtro $n$.

### Filtros Adaptativos e Inserção de Ruído
* **Filtro Adaptativo de Mediana:** Remoção progressiva de ruído preservando detalhes com tamanho máximo de janela $S_{max}$ configurável.
* **Ruído Aditivo Gaussiano:** Inserção de ruído com controle de média $\mu$ e desvio padrão $\sigma$.
* **Ruído Sal e Pimenta:** Inserção de ruído pontual com controle de densidade e proporção sal/pimenta.

---

## Requisitos Técnicos e Regras de Negócio

* **Formatos Aceitos:** Imagens `.png` (RGB de 24 bits ou Escala de Cinza de 8 bits).
* **Habilitação/Desabilitação Dinâmica:** Operações exclusivas para escala de cinza (ex: Equalização de Histograma) tratam ou alertam automaticamente sobre imagens coloridas.
* **Visualização:** Comparação lado a lado entre a imagem original e os resultados.
* **Exportação:** Botão de download para salvar os resultados processados em arquivo `.png`.
* **Métricas:** Exibição de dimensões, menor/maior intensidade e média de tons de cinza.

---

## Estrutura do Repositório

```text
.
├── app.py                          # Ponto de entrada da aplicação Streamlit (orquestração)
├── requirements.txt                # Dependências do Python
├── README.md                       # Documentação do projeto
│
├── assets/                         # Imagens/arquivos estáticos usados no projeto
│
├── processing/                     # Módulos de processamento, separados por categoria
│   ├── color/
│   │   ├── rgb_decomposition.py    # Decomposição em componentes RGB
│   │   └── hsv_decomposition.py    # Decomposição em componentes HSV
│   │
│   ├── grayscale/
│   │   ├── thresholding.py         # Limiarização
│   │   ├── intensity_transform.py  # Transformações log/potência e fatiamento por intensidade
│   │   └── histogram_eq.py         # Equalização de histograma
│   │
│   ├── spatial/
│   │   ├── smoothing.py            # Filtros de média gaussiana, mediana, mínimo e máximo
│   │   ├── sharpening.py           # Máscara de aguçamento
│   │   ├── edge_detection.py       # Realce por Laplaciano e gradiente de Sobel
│   │   ├── noise.py                # Ruído aditivo gaussiano e ruído sal e pimenta
│   │   └── adaptive_median.py      # Filtro adaptativo de mediana
│   │
│   └── frequency/
│       ├── fft_utils.py            # Utilitários de FFT usados pelos filtros de frequência
│       ├── gaussian_filters.py     # Filtros passa-alta/passa-baixa gaussianos
│       └── butterworth_filters.py  # Filtros passa-alta/passa-baixa de Butterworth
│
├── ui/                              # Componentes de interface
│   ├── sidebar.py                  # Catálogo de processos e seleção na barra lateral
│   └── display.py                  # Upload, exibição de imagens, parâmetros e downloads
│
└── utils/                           # Utilidades gerais
    ├── image_io.py                 # Carregamento e exportação de imagens (.png)
    └── validation.py                # Detecção do tipo de imagem e validações

```

## 📋 Pré-requisitos

Para rodar este projeto localmente, você precisará ter instalado em sua máquina:

* [Python 3.10+](https://www.python.org/downloads/)
* Gerenciador de pacotes do Python (`pip`)
* [Git](https://git-scm.com/)

## 🔧 Instruções de Instalação e Execução

**1. Clone o repositório e entre na pasta**

```bash
git clone https://github.com/SEU_USUARIO/Projeto-PDI.git
cd Projeto-PDI

```

**2. Crie o ambiente virtual (venv)**

```bash
python3 -m venv venv

```

**3. Ative o ambiente virtual**

```bash
source venv/bin/activate

```

*(No Windows, use: `venv\Scripts\activate`)*

**4. Instale as dependências**

```bash
pip install -r requirements.txt

```

**5. Execute a aplicação**

```bash
streamlit run app.py
