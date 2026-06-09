import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

# Configuração de página herdada do main.py


# Estilização CSS
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
    
    .metric-val {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00f2fe;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="page-title">🤖 Transparência e Explicabilidade</h1>', unsafe_allow_html=True)
st.write("Análise técnica da performance dos modelos preditivos e a influência das variáveis de satélites nas decisões da IA.")

# Carregar dados e modelos
data_path = "data/dados_ambientais.csv"
model_path_rf = "modelos_salvos/spacerisk_rf_model.joblib"
model_path_dt = "modelos_salvos/spacerisk_dt_model.joblib"
scaler_path = "modelos_salvos/spacerisk_scaler.joblib"
encoders_path = "modelos_salvos/spacerisk_encoders.joblib"

if not (os.path.exists(data_path) and os.path.exists(model_path_rf) and os.path.exists(model_path_dt)):
    st.error("Modelos ou datasets não encontrados. Execute o treinamento do modelo primeiro.")
    st.stop()

# Carregar do disco
df = pd.read_csv(data_path)
rf_model = joblib.load(model_path_rf)
dt_model = joblib.load(model_path_dt)
scaler = joblib.load(scaler_path)
encoders = joblib.load(encoders_path)

# Executar a avaliação no conjunto de teste em tempo real para obter os números exatos
categorical_cols = ["Estado", "Bioma", "Mês", "Uso_Solo"]
df_encoded = df.copy()

for col in categorical_cols:
    df_encoded[col] = encoders[col].transform(df[col])

target_map = {"Baixo": 0, "Médio": 1, "Alto": 2}
df_encoded["Nivel_Risco_Num"] = df_encoded["Nivel_Risco"].map(target_map)

X = df_encoded.drop(columns=["Nivel_Risco", "Nivel_Risco_Num"])
y = df_encoded["Nivel_Risco_Num"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
X_test_scaled = scaler.transform(X_test)

# Predições para avaliação
y_pred_rf = rf_model.predict(X_test_scaled)
y_pred_dt = dt_model.predict(X_test_scaled)

# Métricas
def calcular_metricas(y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average="weighted")
    rec = recall_score(y_true, y_pred, average="weighted")
    f1 = f1_score(y_true, y_pred, average="weighted")
    return acc, prec, rec, f1

acc_rf, prec_rf, rec_rf, f1_rf = calcular_metricas(y_test, y_pred_rf)
acc_dt, prec_dt, rec_dt, f1_dt = calcular_metricas(y_test, y_pred_dt)

# Aba de navegação
tab_metricas, tab_importancia, tab_negocio = st.tabs([
    "📈 Métricas & Comparação", 
    "📊 Importância de Variáveis", 
    "🛡️ Impacto na Decisão da Defesa Civil"
])

with tab_metricas:
    col_desc, col_tab = st.columns([1, 1])
    
    with col_desc:
        st.markdown(
            """
            <div class="premium-card">
                <h3>Desempenho dos Modelos</h3>
                <p>
                    Testamos e avaliamos dois algoritmos clássicos para classificação supervisionada:
                </p>
                <ul>
                    <li><b>Decision Tree (Árvore de Decisão):</b> Modelo interpretável baseado em regras de decisão sequenciais.</li>
                    <li><b>Random Forest (Floresta Aleatória):</b> Conjunto (ensemble) de árvores de decisão combinadas, oferecendo maior acurácia e generalização.</li>
                </ul>
                <p style="font-size:0.9rem; color:#8da4c4;">
                    Ambos foram avaliados usando uma partição de teste contendo 20% das amostras originais (estratificadas).
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col_tab:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### Tabela de Métricas")
        
        tabela_metricas = pd.DataFrame({
            "Métrica": ["Acurácia (Accuracy)", "Precisão (Precision)", "Sensibilidade (Recall)", "F1-Score"],
            "Decision Tree": [f"{acc_dt*100:.2f}%", f"{prec_dt*100:.2f}%", f"{rec_dt*100:.2f}%", f"{f1_dt*100:.2f}%"],
            "Random Forest (Melhor)": [f"{acc_rf*100:.2f}%", f"{prec_rf*100:.2f}%", f"{rec_rf*100:.2f}%", f"{f1_rf*100:.2f}%"]
        })
        st.table(tabela_metricas)
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Matrizes de Confusão
    st.markdown("### 🔲 Matrizes de Confusão (Dados de Teste)")
    col_cm1, col_cm2 = st.columns(2)
    
    classes_labels = ["Baixo", "Médio", "Alto"]
    
    with col_cm1:
        cm_dt = confusion_matrix(y_test, y_pred_dt)
        fig_cm_dt = px.imshow(
            cm_dt,
            text_auto=True,
            x=classes_labels,
            y=classes_labels,
            color_continuous_scale="Blues",
            labels=dict(x="Predito", y="Real"),
            title="Matriz de Confusão: Decision Tree"
        )
        fig_cm_dt.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
        st.plotly_chart(fig_cm_dt, use_container_width=True)
        
    with col_cm2:
        cm_rf = confusion_matrix(y_test, y_pred_rf)
        fig_cm_rf = px.imshow(
            cm_rf,
            text_auto=True,
            x=classes_labels,
            y=classes_labels,
            color_continuous_scale="Greens",
            labels=dict(x="Predito", y="Real"),
            title="Matriz de Confusão: Random Forest"
        )
        fig_cm_rf.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
        st.plotly_chart(fig_cm_rf, use_container_width=True)

with tab_importancia:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### 🧬 Importância das Variáveis (Feature Importance)")
    st.write("Indica quais variáveis mais pesaram nas árvores do Random Forest para classificar o nível de risco.")
    
    importancias = rf_model.feature_importances_
    df_imp = pd.DataFrame({
        "Variável": X.columns,
        "Importância": importancias
    }).sort_values(by="Importância", ascending=True)
    
    fig_imp = px.bar(
        df_imp,
        x="Importância",
        y="Variável",
        orientation="h",
        color="Importância",
        color_continuous_scale="Viridis",
        height=400
    )
    fig_imp.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15, 28, 48, 0.5)',
        font=dict(color="white"),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
    )
    st.plotly_chart(fig_imp, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab_negocio:
    st.markdown(
        """
        <div class="premium-card">
            <h3>🛡️ Justificativa e Impacto Prático na Defesa Civil</h3>
            <p>
                Para coordenadores como <b>Carlos (Defesa Civil)</b>, entender as métricas de IA em termos humanos é vital para salvar vidas e justificar verbas públicas.
            </p>
            <hr style="border-color: rgba(255,255,255,0.1)"/>
            <h4>📌 A Sensibilidade (Recall) como Fator Crítico de Sobrevivência</h4>
            <p>
                Em desastres ambientais, o <b>Falso Negativo</b> (a IA prever risco <i>Baixo</i> quando na verdade o risco era <i>Alto</i>) é o pior cenário possível.
                Isso faria com que a Defesa Civil não emitisse alertas, resultando em comunidades pegas de surpresa por enchentes ou incêndios.
                Por isso, buscamos maximizar o <b>Recall para a classe de Alto Risco</b>, garantindo que o maior número possível de ameaças reais seja detectado preventivamente.
            </p>
            <h4>📌 A Precisão (Precision) como Fator de Credibilidade e Economia</h4>
            <p>
                O <b>Falso Positivo</b> (a IA prever risco <i>Alto</i> quando é <i>Baixo</i>) gera alarmes falsos. Embora não resulte em perdas humanas diretas, 
                falsos positivos constantes cansam a população (efeito "Menino e o Lobo"), fazendo com que ignorem alertas futuros, 
                além de desperdiçar recursos financeiros deslocando equipes desnecessariamente.
            </p>
            <h4>📌 ODS da ONU Atingidos</h4>
            <p>
                O equilíbrio de precisão e sensibilidade deste modelo apoia diretamente a construção de <b>Cidades e Comunidades Sustentáveis (ODS 11)</b> 
                e a <b>Ação Contra as Mudanças Pluviométricas e de Clima (ODS 13)</b>.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
