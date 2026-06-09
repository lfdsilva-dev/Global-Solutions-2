import streamlit as st
import pandas as pd
import os

# Configuração de página herdada do main.py


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
    
    .alert-card-alto {
        background: rgba(239, 85, 59, 0.12);
        border: 1px solid rgba(239, 85, 59, 0.4);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 6px solid #EF553B;
    }
    
    .alert-card-medio {
        background: rgba(254, 203, 82, 0.08);
        border: 1px solid rgba(254, 203, 82, 0.3);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 6px solid #FECB52;
    }
    
    .page-title {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.2rem;
        margin-bottom: 5px;
    }
    
    .badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    
    .badge-alto {
        background-color: #EF553B;
        color: white;
    }
    
    .badge-medio {
        background-color: #FECB52;
        color: #1e1e1e;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="page-title">⚠️ Central de Alertas</h1>', unsafe_allow_html=True)
st.write("Alertas preditivos automáticos gerados a partir do monitoramento em tempo real de variáveis críticas.")

# Carregar dados
data_path = "data/dados_ambientais.csv"
if not os.path.exists(data_path):
    st.error("Dataset 'data/dados_ambientais.csv' não encontrado.")
    st.stop()

df = pd.read_csv(data_path)

# Filtrar apenas Médio e Alto Risco para Alertas
df_alertas = df[df["Nivel_Risco"].isin(["Alto", "Médio"])].copy()

# Barra lateral
with st.sidebar:
    st.markdown("### 🚨 Filtros de Alertas")
    filtro_estado = st.selectbox("Filtrar por Estado:", ["Todos"] + list(df_alertas["Estado"].unique()))
    filtro_nivel = st.radio("Grau de Severidade:", ["Todos", "Apenas Alto Risco", "Apenas Médio Risco"])

# Aplicar filtros da barra lateral
if filtro_estado != "Todos":
    df_alertas = df_alertas[df_alertas["Estado"] == filtro_estado]

if filtro_nivel == "Apenas Alto Risco":
    df_alertas = df_alertas[df_alertas["Nivel_Risco"] == "Alto"]
elif filtro_nivel == "Apenas Médio Risco":
    df_alertas = df_alertas[df_alertas["Nivel_Risco"] == "Médio"]

# Exibir quantidade
st.markdown(f"**{len(df_alertas)}** alertas ativos identificados.")

if df_alertas.empty:
    st.success("Nenhum alerta pendente para a seleção atual.")
else:
    # Mostrar os primeiros 15 alertas para não sobrecarregar a página
    alertas_exibir = df_alertas.head(15)
    
    for idx, row in alertas_exibir.iterrows():
        # Identificar tipo de risco e recomendação
        # 1. Risco de Queimada
        if row["Focos_Calor"] > 10 or (row["Temperatura"] > 32 and row["Umidade"] < 35):
            tipo_risco = "Incêndio Florestal / Queimada"
            fatores = f"Temperatura de {row['Temperatura']}°C, umidade do ar extremamente baixa ({row['Umidade']}%), presença de {row['Focos_Calor']} focos de calor ativos e cobertura de solo do tipo '{row['Uso_Solo']}'."
            recomendacao = "Intensificar o monitoramento por brigadas, acionar a Defesa Civil local para prevenção de queimadas, proibir atividades de manejo de fogo e emitir avisos sonoros e digitais à população rural."
        # 2. Risco de Deslizamento
        elif row["Precipitacao"] > 150 and row["Declividade"] > 20:
            tipo_risco = "Deslizamento de Encosta"
            fatores = f"Precipitação acumulada severa ({row['Precipitacao']} mm) incidindo em relevo montanhoso com {row['Declividade']}° de declividade."
            recomendacao = "Alertar moradores em áreas de encosta, acionar plano de evacuação preventiva para abrigos temporários e monitorar índices pluviométricos nas próximas 12 horas."
        # 3. Risco de Enchente
        elif row["Precipitacao"] > 120 and (row["Uso_Solo"] == "Área Urbana" or row["Distancia_Rios"] < 200):
            tipo_risco = "Alagamento / Inundação Gradual"
            fatores = f"Precipitação de {row['Precipitacao']} mm em área altamente urbanizada ou com proximidade crítica a rios ({row['Distancia_Rios']:.1f} m)."
            recomendacao = "Limpar bueiros e canais de drenagem, monitorar nível dos rios locais, bloquear vias com histórico de alagamento e orientar motoristas a evitarem áreas baixas."
        # 4. Geral
        else:
            tipo_risco = "Instabilidade Climática"
            fatores = f"Anomalia combinada de precipitação ({row['Precipitacao']} mm) e temperatura ({row['Temperatura']}°C) na cobertura vegetal do tipo {row['Bioma']}."
            recomendacao = "Manter equipes em estado de prontidão e atualizar os dados do sensor nas próximas 6 horas."
            
        card_class = "alert-card-alto" if row["Nivel_Risco"] == "Alto" else "alert-card-medio"
        badge_class = "badge-alto" if row["Nivel_Risco"] == "Alto" else "badge-medio"
        label_risco = "Risco Alto" if row["Nivel_Risco"] == "Alto" else "Risco Médio"
        
        st.markdown(
            f"""
            <div class="{card_class}">
                <span class="badge {badge_class}">{label_risco}</span>
                <h4 style="margin: 0 0 8px 0; color: #f0f2f6;">🚨 {tipo_risco} - Região de Coordenadas ({row['Latitude']:.4f}, {row['Longitude']:.4f})</h4>
                <p style="margin: 0 0 10px 0; font-size: 0.9rem;"><b>Localização:</b> Estado de {row['Estado']} | Bioma: {row['Bioma']} | Uso do Solo: {row['Uso_Solo']}</p>
                <p style="margin: 0 0 10px 0; font-size: 0.88rem; color: #cdd9e5;"><b>Fatores Determinantes:</b> {fatores}</p>
                <div style="background: rgba(255, 255, 255, 0.05); padding: 12px; border-radius: 8px; font-size: 0.85rem; border-left: 3px solid #4facfe;">
                    <b>Recomendação Técnica:</b> {recomendacao}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
