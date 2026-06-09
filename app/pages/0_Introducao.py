import streamlit as st

# Estilização CSS customizada
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(10, 20, 38, 1) 0%, rgba(20, 32, 54, 1) 90%);
        color: #f0f2f6;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #0b1322 !important;
        border-right: 1px solid #1e2d4a;
    }
    
    .premium-card {
        background: rgba(30, 45, 74, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    .gradient-title {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.8rem;
        margin-bottom: 0px;
    }
    
    .gradient-subtitle {
        color: #8da4c4;
        font-size: 1.15rem;
        margin-bottom: 25px;
    }
    
    .ods-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
        color: #fff;
    }
</style>
""", unsafe_allow_html=True)

# Barra Lateral
with st.sidebar:
    st.markdown("<h1 style='text-align: center; margin-top: -10px; margin-bottom: 10px;'>🛰️</h1>", unsafe_allow_html=True)
    st.markdown("### **SpaceRisk AI**")
    st.markdown("Previsão inteligente de riscos ambientais com IA e dados espaciais.")
    st.divider()
    st.info("Utilize as páginas do menu lateral para navegar nas análises e previsões.")

# Conteúdo Principal
st.markdown('<h1 class="gradient-title">SpaceRisk AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="gradient-subtitle">Previsão inteligente de riscos ambientais com dados espaciais</p>', unsafe_allow_html=True)

# Layout de duas colunas
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        """
        <div class="premium-card">
            <h3>🌍 O que é o SpaceRisk AI?</h3>
            <p>
                O SpaceRisk AI é uma plataforma inteligente voltada para a antecipação de riscos ambientais nas diversas regiões brasileiras.
                Ao cruzar dados geoespaciais, climáticos e históricos obtidos de satélites e sensores públicos, a solução aplica modelos avançados de
                Machine Learning para gerar classificações claras e acionáveis de risco ambiental (Baixo, Médio ou Alto).
            </p>
            <p>
                A proposta visa empoderar tomadores de decisão — como a Defesa Civil, prefeituras municipais e produtores rurais — 
                para agirem de forma preventiva e reduzirem perdas ambientais, econômicas e humanas causadas por queimadas e enchentes.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div class="premium-card">
            <h3>👥 Integrantes da Equipe (Turma 2TSCOR)</h3>
            <ul>
                <li><b>Luiz Felipe Duarte Silva</b> - RM 559675</li>
                <li><b>Mateus Florencio Macedo</b> - RM 560446</li>
                <li><b>Mickael Fabris dos Anjos</b> - RM 560577</li>
                <li><b>Pedro Luiz dos Passos Aguiar</b> - RM 560096</li>
                <li><b>Nicolas Samuel Crisostomo Neri</b> - RM 561034</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="premium-card">
            <h3>🤝 Parceiro Estratégico</h3>
            <p><b>Pacto Global da ONU</b></p>
            <p style="font-size: 0.9rem; color: #8da4c4;">
                Solução desenvolvida em alinhamento aos Objetivos de Desenvolvimento Sustentável (ODS) para combater os efeitos das mudanças climáticas globais.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("### Objetivos de Desenvolvimento Sustentável (ODS)")
    st.markdown(
        """
        <span class="ods-badge" style="background-color: #e5243b;">ODS 3: Saúde e Bem-estar</span>
        <span class="ods-badge" style="background-color: #f99d1c;">ODS 9: Indústria e Inovação</span>
        <span class="ods-badge" style="background-color: #f36d25;">ODS 11: Cidades Sustentáveis</span>
        <span class="ods-badge" style="background-color: #3f7e44;">ODS 13: Ação Contra o Clima</span>
        <span class="ods-badge" style="background-color: #56c02b;">ODS 15: Vida Terrestre</span>
        """,
        unsafe_allow_html=True
    )

st.divider()
st.markdown("### **Como começar?**")
st.write("Selecione uma das opções no menu à esquerda:")
col_nav1, col_nav2, col_nav3 = st.columns(3)

with col_nav1:
    st.markdown(
        """
        <div style="background: rgba(30, 45, 74, 0.2); padding: 20px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);">
            <h4>📊 Dashboard Geral</h4>
            <p style="font-size: 0.9rem; color: #8da4c4;">Acompanhe o mapa de risco dinâmico, KPIs de calor, chuva e filtros de estados e biomas.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col_nav2:
    st.markdown(
        """
        <div style="background: rgba(30, 45, 74, 0.2); padding: 20px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);">
            <h4>⚠️ Central de Alertas</h4>
            <p style="font-size: 0.9rem; color: #8da4c4;">Veja as notificações preventivas, os fatores críticos de influência e recomendações acionáveis.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col_nav3:
    st.markdown(
        """
        <div style="background: rgba(30, 45, 74, 0.2); padding: 20px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);">
            <h4>🤖 Inteligência Artificial</h4>
            <p style="font-size: 0.9rem; color: #8da4c4;">Consulte a explicabilidade do modelo, as métricas obtidas e a importância de cada variável de satélite.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
