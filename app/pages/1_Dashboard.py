import streamlit as st
import pandas as pd
import plotly.express as px
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
    
    .premium-card {
        background: rgba(30, 45, 74, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
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
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="page-title">📊 Dashboard Geral de Riscos</h1>', unsafe_allow_html=True)
st.write("Análise em tempo real de áreas monitoradas e classificação de riscos ambientais.")

# Carregar dados
data_path = "data/dados_ambientais.csv"
if not os.path.exists(data_path):
    st.error("Dataset 'data/dados_ambientais.csv' não encontrado. Por favor, gere o dataset primeiro.")
    st.stop()

df = pd.read_csv(data_path)

# Barra Lateral - Filtros
with st.sidebar:
    st.markdown("### 🔍 Filtros de Análise")
    
    # Filtro por Estado
    lista_estados = sorted(df["Estado"].unique())
    estados_selecionados = st.multiselect("Estados:", lista_estados, default=lista_estados)
    
    # Filtro por Bioma
    lista_biomas = sorted(df["Bioma"].unique())
    biomas_selecionados = st.multiselect("Biomas:", lista_biomas, default=lista_biomas)
    
    # Filtro por Uso do Solo
    lista_usos = sorted(df["Uso_Solo"].unique())
    usos_selecionados = st.multiselect("Uso do Solo:", lista_usos, default=lista_usos)
    
    # Filtro por Nível de Risco
    riscos_selecionados = st.multiselect("Nível de Risco:", ["Baixo", "Médio", "Alto"], default=["Baixo", "Médio", "Alto"])

# Aplicar filtros
df_filtered = df[
    (df["Estado"].isin(estados_selecionados)) &
    (df["Bioma"].isin(biomas_selecionados)) &
    (df["Uso_Solo"].isin(usos_selecionados)) &
    (df["Nivel_Risco"].isin(riscos_selecionados))
]

if df_filtered.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
    st.stop()

# KPIs no topo
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

total_areas = len(df_filtered)
areas_alto_risco = len(df_filtered[df_filtered["Nivel_Risco"] == "Alto"])
perc_alto_risco = (areas_alto_risco / total_areas) * 100 if total_areas > 0 else 0
temp_media = df_filtered["Temperatura"].mean()
focos_calor_total = df_filtered["Focos_Calor"].sum()

with col_kpi1:
    st.markdown(
        f"""
        <div class="premium-card" style="text-align: center;">
            <p style="margin:0; font-size:0.9rem; color:#8da4c4;">Áreas Monitoradas</p>
            <h2 style="margin:5px 0; color:#4facfe;">{total_areas}</h2>
            <p style="margin:0; font-size:0.75rem; color:#8da4c4;">regiões filtradas</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_kpi2:
    st.markdown(
        f"""
        <div class="premium-card" style="text-align: center; border-left: 4px solid #ff4b4b;">
            <p style="margin:0; font-size:0.9rem; color:#8da4c4;">Alto Risco</p>
            <h2 style="margin:5px 0; color:#ff4b4b;">{areas_alto_risco}</h2>
            <p style="margin:0; font-size:0.75rem; color:#ff4b4b;">{perc_alto_risco:.1f}% do total</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_kpi3:
    st.markdown(
        f"""
        <div class="premium-card" style="text-align: center;">
            <p style="margin:0; font-size:0.9rem; color:#8da4c4;">Temperatura Média</p>
            <h2 style="margin:5px 0; color:#ffb03a;">{temp_media:.1f}°C</h2>
            <p style="margin:0; font-size:0.75rem; color:#8da4c4;">faixa de dados selecionada</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_kpi4:
    st.markdown(
        f"""
        <div class="premium-card" style="text-align: center;">
            <p style="margin:0; font-size:0.9rem; color:#8da4c4;">Focos de Calor Acumulados</p>
            <h2 style="margin:5px 0; color:#ff7a00;">{focos_calor_total}</h2>
            <p style="margin:0; font-size:0.75rem; color:#8da4c4;">detectados por satélites</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Linha 1: Mapa + Distribuição de risco
col_map, col_pie = st.columns([2, 1])

with col_map:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### 🗺️ Visualização Geoespacial de Riscos")
    
    # Criar mapa interativo com Plotly
    fig_map = px.scatter_mapbox(
        df_filtered,
        lat="Latitude",
        lon="Longitude",
        color="Nivel_Risco",
        color_discrete_map={"Baixo": "#00CC96", "Médio": "#FECB52", "Alto": "#EF553B"},
        category_orders={"Nivel_Risco": ["Baixo", "Médio", "Alto"]},
        hover_data=["Estado", "Bioma", "Temperatura", "Umidade", "Precipitacao", "Uso_Solo"],
        zoom=3.2,
        height=450,
        mapbox_style="carto-darkmatter"
    )
    fig_map.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            title="Nível de Risco",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(10, 20, 38, 0.8)",
            font=dict(color="white")
        )
    )
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_pie:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Proporção de Riscos")
    
    # Gráfico de Rosca (Donut Chart)
    risco_counts = df_filtered["Nivel_Risco"].value_counts().reset_index()
    risco_counts.columns = ["Nivel_Risco", "Quantidade"]
    
    fig_pie = px.pie(
        risco_counts,
        names="Nivel_Risco",
        values="Quantidade",
        hole=0.4,
        color="Nivel_Risco",
        color_discrete_map={"Baixo": "#00CC96", "Médio": "#FECB52", "Alto": "#EF553B"},
        category_orders={"Nivel_Risco": ["Baixo", "Médio", "Alto"]}
    )
    fig_pie.update_layout(
        margin={"r":10,"t":30,"l":10,"b":10},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5, font=dict(color="white"))
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Linha 2: Clima por Risco (Scatter) + Risco por Estado (Bar)
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### 🌡️ Relação Climatológica e Risco")
    
    fig_scatter = px.scatter(
        df_filtered,
        x="Temperatura",
        y="Umidade",
        color="Nivel_Risco",
        color_discrete_map={"Baixo": "#00CC96", "Médio": "#FECB52", "Alto": "#EF553B"},
        category_orders={"Nivel_Risco": ["Baixo", "Médio", "Alto"]},
        labels={"Temperatura": "Temperatura (°C)", "Umidade": "Umidade Relativa (%)"},
        opacity=0.7,
        height=350
    )
    fig_scatter.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15, 28, 48, 0.5)',
        font=dict(color="white"),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_chart2:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### 🏛️ Distribuição de Áreas Críticas por Estado")
    
    # Agrupar dados
    estado_risco = df_filtered.groupby(["Estado", "Nivel_Risco"]).size().reset_index(name="Quantidade")
    
    fig_bar = px.bar(
        estado_risco,
        x="Estado",
        y="Quantidade",
        color="Nivel_Risco",
        color_discrete_map={"Baixo": "#00CC96", "Médio": "#FECB52", "Alto": "#EF553B"},
        category_orders={"Nivel_Risco": ["Baixo", "Médio", "Alto"]},
        barmode="group",
        height=350
    )
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15, 28, 48, 0.5)',
        font=dict(color="white"),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
