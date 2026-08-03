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


## Estrutura do Repositório

```text
.
├── app.py                          # Ponto de entrada da aplicação Streamlit (orquestração)
├── requirements.txt                # Dependências do Python
├── Dockerfile                      # Instruções para construção da imagem Docker
├── docker-compose.yml              # Orquestração do container
├── README.md                       # Documentação do projeto
├── projeto.pdf                     # Especificações originais do projeto
│
├── assets/                         # Imagens/arquivos estáticos usados no projeto
│
├── processing/                     # Módulos de processamento, separados por categoria
│   ├── color/                      # RGB e HSV
│   ├── grayscale/                  # Limiarização, transformações log/gamma e histograma
│   ├── spatial/                    # Filtros espaciais, aguçamento, bordas e ruídos
│   └── frequency/                  # Filtros de Fourier (Gaussiano e Butterworth)
│
├── ui/                             # Componentes de interface
│   ├── sidebar.py                  # Catálogo de processos e seleção na barra lateral
│   └── display.py                  # Upload, exibição de imagens, parâmetros e downloads
│
└── utils/                          # Utilidades gerais
    ├── image_io.py                 # Carregamento e exportação de imagens (.png)
    └── validation.py               # Detecção do tipo de imagem e validações

```

---

## 📋 Pré-requisitos

Para rodar este projeto, escolha uma das opções abaixo e certifique-se de ter as ferramentas necessárias instaladas:

**Opção 1: Via Docker (Recomendado)**

* [Docker](https://www.docker.com/products/docker-desktop/) e Docker Compose instalados.
* [Git](https://git-scm.com/)

**Opção 2: Localmente via Python**

* [Python 3.10+](https://www.python.org/downloads/) e `pip`
* [Git](https://git-scm.com/)

---

## 🔧 Instruções de Instalação e Execução

Primeiro, clone o repositório em sua máquina:

```bash
git clone https://github.com/SEU_USUARIO/Projeto-PDI.git
cd Projeto-PDI

```

### 🐳 Opção 1: Executando com Docker (Recomendado)

Esta é a maneira mais simples, pois isola completamente a aplicação e suas dependências.

**1. Construa e inicie o container:**

```bash
docker-compose up --build

```

**2. Acesse a aplicação:**
Abra o seu navegador e acesse `http://localhost:8501`.

*(Para parar a execução, pressione `Ctrl+C` no terminal ou rode `docker-compose down`).*

---

### 💻 Opção 2: Executando Localmente (Com venv)

Caso deseje rodar a aplicação diretamente no seu sistema operacional para modificar o código e ver as alterações em tempo real.

**1. Crie o ambiente virtual (venv)**

```bash
python3 -m venv venv

```

**2. Ative o ambiente virtual**

```bash
source venv/bin/activate

```

*(No Windows, use: `venv\Scripts\activate`)*

**3. Instale as dependências**

```bash
pip install -r requirements.txt

```

**4. Execute a aplicação**

```bash
streamlit run app.py

```

*(O Streamlit abrirá automaticamente uma aba no seu navegador padrão no endereço `http://localhost:8501`).*

