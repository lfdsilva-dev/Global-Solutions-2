import streamlit as st

st.set_page_config(
    page_title="SpaceRisk AI - Previsão de Risco Ambiental",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Definir as páginas da aplicação com títulos, ícones e URLs corretas
intro_page = st.Page("pages/0_Introducao.py", title="Introdução", icon="🌍", default=True)
dashboard_page = st.Page("pages/1_Dashboard.py", title="Dashboard", icon="📊")
alerts_page = st.Page("pages/2_Alertas.py", title="Alertas", icon="⚠️")
regiao_page = st.Page("pages/3_Regiao.py", title="Região", icon="🔍")
explicabilidade_page = st.Page("pages/4_Explicabilidade.py", title="Explicabilidade", icon="🤖")

# Criar a barra de navegação personalizada no menu lateral esquerdo
pg = st.navigation([intro_page, dashboard_page, alerts_page, regiao_page, explicabilidade_page])

# Executar a página ativa selecionada pelo usuário
pg.run()
