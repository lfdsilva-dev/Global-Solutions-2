import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.graph_objects as go

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
    
    .premium-card {
        background: rgba(30, 45, 74, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
    }
    
    .page-title {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.2rem;
        margin-bottom: 5px;
    }
    
    .prediction-box-baixo {
        background-color: rgba(0, 204, 150, 0.15);
        border: 2px solid #00CC96;
        color: #00CC96;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        font-weight: bold;
        font-size: 1.5rem;
    }
    
    .prediction-box-medio {
        background-color: rgba(254, 203, 82, 0.15);
        border: 2px solid #FECB52;
        color: #FECB52;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        font-weight: bold;
        font-size: 1.5rem;
    }
    
    .prediction-box-alto {
        background-color: rgba(239, 85, 59, 0.15);
        border: 2px solid #EF553B;
        color: #EF553B;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        font-weight: bold;
        font-size: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="page-title">🔍 Análise Regional & Simulação</h1>', unsafe_allow_html=True)
st.write("Simule condições ambientais e veja a previsão do modelo de IA em tempo real.")

# Carregar artefatos de ML
caminho_modelo = "modelos_salvos/spacerisk_rf_model.joblib"
caminho_scaler = "modelos_salvos/spacerisk_scaler.joblib"
caminho_encoders = "modelos_salvos/spacerisk_encoders.joblib"

if not (os.path.exists(caminho_modelo) and os.path.exists(caminho_scaler) and os.path.exists(caminho_encoders)):
    st.error("Artefatos do modelo de Machine Learning não encontrados. Execute o treinamento primeiro.")
    st.stop()

# Carregar objetos
rf_model = joblib.load(caminho_modelo)
scaler = joblib.load(caminho_scaler)
encoders = joblib.load(caminho_encoders)

# Layout de duas colunas
col_sim, col_pred = st.columns([1, 1])

with col_sim:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### 🎛️ Parâmetros Climáticos e Geográficos")
    st.write("Ajuste as condições da região para simular o risco:")
    
    # Inputs categóricos usando as classes do LabelEncoder
    estado = st.selectbox("Estado (Localidade):", encoders["Estado"].classes_)
    bioma = st.selectbox("Bioma Predominante:", encoders["Bioma"].classes_)
    mes = st.selectbox("Mês de Referência:", encoders["Mês"].classes_)
    uso_solo = st.selectbox("Cobertura do Solo (Uso):", encoders["Uso_Solo"].classes_)
    
    # Coordenadas geográficas baseadas no estado
    coordenadas_base = {
        "SP": (-23.55, -46.63), "MG": (-18.51, -44.55), "AM": (-3.47, -62.22),
        "MT": (-12.68, -56.92), "BA": (-12.58, -41.70), "RS": (-30.03, -51.23),
        "GO": (-15.83, -49.84), "PA": (-5.54, -52.73), "CE": (-5.10, -39.65),
        "PR": (-24.89, -51.55)
    }
    lat_base, lon_base = coordenadas_base.get(estado, (-15.78, -47.93))
    
    # Inputs de coordenadas
    lat = st.number_input("Latitude:", value=lat_base, format="%.5f")
    lon = st.number_input("Longitude:", value=lon_base, format="%.5f")
    
    # Sliders para variáveis contínuas
    temp = st.slider("Temperatura (°C):", min_value=15.0, max_value=45.0, value=28.0, step=0.5)
    umidade = st.slider("Umidade Relativa do Ar (%):", min_value=5.0, max_value=100.0, value=60.0, step=1.0)
    chuva = st.slider("Precipitação Pluviométrica (mm):", min_value=0.0, max_value=500.0, value=50.0, step=5.0)
    ndvi = st.slider("Índice de Vegetação (NDVI):", min_value=-0.2, max_value=1.0, value=0.6, step=0.05)
    focos = st.slider("Focos de Calor Recentes (Satélites):", min_value=0, max_value=150, value=5, step=1)
    declive = st.slider("Declividade do Terreno (Graus):", min_value=0.0, max_value=45.0, value=12.0, step=1.0)
    dist_rios = st.slider("Distância do Rio mais próximo (m):", min_value=0, max_value=5000, value=1200, step=100)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Processar entrada para predição
# Codificar variáveis de texto
estado_encoded = encoders["Estado"].transform([estado])[0]
bioma_encoded = encoders["Bioma"].transform([bioma])[0]
mes_encoded = encoders["Mês"].transform([mes])[0]
uso_solo_encoded = encoders["Uso_Solo"].transform([uso_solo])[0]

# Construir DataFrame de entrada no formato exato das features do treino
dados_entrada = pd.DataFrame([{
    "Estado": estado_encoded,
    "Bioma": bioma_encoded,
    "Latitude": lat,
    "Longitude": lon,
    "Mês": mes_encoded,
    "Temperatura": temp,
    "Umidade": umidade,
    "Precipitacao": chuva,
    "NDVI": ndvi,
    "Focos_Calor": focos,
    "Declividade": declive,
    "Distancia_Rios": dist_rios,
    "Uso_Solo": uso_solo_encoded
}])

# Padronizar
dados_entrada_scaled = scaler.transform(dados_entrada)

# Predição
predicao = rf_model.predict(dados_entrada_scaled)[0]
probabilidade = rf_model.predict_proba(dados_entrada_scaled)[0]

with col_pred:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### 🔮 Previsão do Modelo de Machine Learning")
    st.write("Abaixo está o nível de risco previsto pelo Random Forest Classifier para as condições atuais:")
    
    # Exibir resultado com estilização condicional
    classes = ["Baixo", "Médio", "Alto"]
    resultado_risco = classes[predicao]
    
    if resultado_risco == "Baixo":
        st.markdown('<div class="prediction-box-baixo">🟢 Risco Previsto: BAIXO</div>', unsafe_allow_html=True)
        cor_destaque = "#00CC96"
        detalhe_risco = "Região segura nas condições simuladas. O ecossistema está equilibrado e a probabilidade de fogo descontrolado ou alagamento severo é reduzida."
    elif resultado_risco == "Médio":
        st.markdown('<div class="prediction-box-medio">🟡 Risco Previsto: MÉDIO</div>', unsafe_allow_html=True)
        cor_destaque = "#FECB52"
        detalhe_risco = "Atenção recomendada. As variáveis indicam um risco moderado. Fatores como temperatura elevada combinada com declive médio exigem monitoramento preventivo regular."
    else:
        st.markdown('<div class="prediction-box-alto">🔴 Risco Previsto: ALTO</div>', unsafe_allow_html=True)
        cor_destaque = "#EF553B"
        detalhe_risco = "Alerta Crítico! A IA prevê alta probabilidade de desastres ecológicos (como focos de incêndios em áreas secas ou alagamento de encostas sob chuvas fortes). Mobilização preventiva é necessária."
        
    st.markdown(f"<p style='margin-top:15px; font-size:0.95rem; line-height:1.5;'><b>Avaliação Técnica:</b> {detalhe_risco}</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Gráfico de gauge de certeza da previsão
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Probabilidade da IA por Classe")
    
    fig_prob = go.Figure(go.Bar(
        x=[prob * 100 for prob in probabilidade],
        y=["Baixo Risco ", "Médio Risco ", "Alto Risco "],
        orientation='h',
        marker=dict(
            color=['#00CC96', '#FECB52', '#EF553B'],
            line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
        )
    ))
    
    fig_prob.update_layout(
        xaxis=dict(title="Certeza do Modelo (%)", range=[0, 100], gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15, 28, 48, 0.5)',
        font=dict(color="white"),
        margin=dict(l=100, r=10, t=10, b=10),
        height=250
    )
    
    st.plotly_chart(fig_prob, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
