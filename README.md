# SpaceRisk AI 🌍
### Previsão inteligente de riscos ambientais com dados espaciais

Este repositório contém a solução desenvolvida para a **Global Solution 2026** da **FIAP**, realizada em parceria estratégica com o **Pacto Global da ONU**. A proposta do **SpaceRisk AI** é aliar Data Science, Inteligência Artificial e dados ambientais espaciais para prever níveis de risco ecológico em regiões do Brasil, oferecendo alertas e suporte de decisão preventiva a órgãos como a Defesa Civil.

---

## 👥 Integrantes da Equipe (Turma 2TSCOR)
- **Luiz Felipe Duarte Silva** - RM 559675
- **Mateus Florencio Macedo** - RM 560446
- **Mickael Fabris dos Anjos** - RM 560577
- **Pedro Luiz dos Passos Aguiar** - RM 560096
- **Nicolas Samuel Crisostomo Neri** - RM 561034

---

## 🛠️ Tecnologias Utilizadas
- **Linguagem Principal:** Python 3.10+
- **Análise & Modelagem:** Pandas, NumPy, Scikit-learn, Joblib
- **Visualização de Dados:** Plotly Express, Plotly Graph Objects
- **Interface & Dashboard:** Streamlit (Layout Web Responsivo e Tematização Dark Mode Premium)

---

## 📁 Estrutura do Projeto
```text
├── app/
│   ├── main.py                     # Script principal (Home / ODS / Apresentação)
│   └── pages/
│       ├── 1_Dashboard.py          # Dashboard Geral (Mapa interativo e Gráficos de Clima)
│       ├── 2_Alertas.py            # Central de Alertas (Notificações lógicas para Defesa Civil)
│       ├── 3_Regiao.py             # Simulação e Predição da IA em Tempo Real
│       └── 4_Explicabilidade.py    # Explicabilidade do Modelo (Importância de variáveis e CM)
├── data/
│   ├── gerar_dados.py              # Script para geração de dataset sintético realista
│   └── dados_ambientais.csv        # Dataset gerado (coordenadas, clima e cobertura de solo)
├── modelos_salvos/                 # Modelos treinados e pré-processadores (.joblib)
├── notebooks/
│   ├── spacerisk_ml.ipynb          # Jupyter Notebook oficial com EDA, Treino e Avaliação
│   └── executar_treinamento.py     # Script para treinar e exportar modelos em lote
├── linkvideo.txt                   # Arquivo contendo o link do Pitch do YouTube
├── requirements.txt                # Dependências necessárias do Python
└── README.md                       # Documentação do projeto
```

---

## 🚀 Como Rodar o Projeto

Siga as instruções passo a passo para instalar e executar a aplicação em sua máquina local.

### 1. Clonar ou Acessar o Diretório
Abra o terminal na raiz do projeto onde os arquivos estão localizados.

### 2. Instalar Dependências
Instale todas as bibliotecas necessárias listadas no `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Gerar o Dataset Ambiental
Gere o dataset inicial de variáveis de satélites e sensores (coordenadas brasileiras, temperatura, umidade, NDVI, declividade, etc.):
```bash
python data/gerar_dados.py
```
Isso criará a planilha `data/dados_ambientais.csv`.

### 4. Treinar e Exportar os Modelos de IA
Execute o script de treinamento para criar e salvar a **Decision Tree** e a **Random Forest**:
```bash
python notebooks/executar_treinamento.py
```
Esse processo salvará os modelos e scalers na pasta `modelos_salvos/` para uso do Dashboard.

### 5. Iniciar a Aplicação Web (Streamlit)
Rode o servidor local do Streamlit:
```bash
streamlit run app/main.py
```
A aplicação abrirá automaticamente em seu navegador padrão (geralmente no endereço `http://localhost:8501`).

---

## 📖 Funcionalidades do Dashboard

1. **Página Inicial:** Contextualização do projeto, parceiro (ONU), metas ODS e lista de integrantes.
2. **Dashboard Geral:** Filtros avançados por Estado, Bioma e Cobertura de Solo; Mapa de calor geoespacial dinâmico e gráficos cruzando temperatura, umidade e severidade.
3. **Central de Alertas:** Análise automatizada indicando riscos específicos (queimadas por seca, deslizamento por chuvas em encostas, alagamentos em áreas urbanas) e exibição de planos de ação recomendados para a Defesa Civil municipal.
4. **Simulação por Região:** Controle de sliders climáticos (temperatura, umidade, NDVI, chuva) para simular previsões de risco do modelo Random Forest em tempo real.
5. **Explicabilidade:** Comparação de métricas (Acurácia, Precisão, Sensibilidade, F1-Score) entre modelos, plot de matrizes de confusão e gráfico indicando a importância relativa das variáveis.
