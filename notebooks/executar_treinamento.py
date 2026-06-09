import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import joblib

# Carregar dados
data_path = "data/dados_ambientais.csv"
if not os.path.exists(data_path):
    print("Dataset não encontrado. Certifique-se de executar a partir da raiz do projeto.")
    exit(1)

df = pd.read_csv(data_path)
print(f"Dataset carregado com {df.shape[0]} amostras.")

# Codificar categóricas
categorical_cols = ["Estado", "Bioma", "Mês", "Uso_Solo"]
encoders = {}
df_encoded = df.copy()

for col in categorical_cols:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df[col])
    encoders[col] = le

# Mapear alvo
target_map = {"Baixo": 0, "Médio": 1, "Alto": 2}
df_encoded["Nivel_Risco_Num"] = df_encoded["Nivel_Risco"].map(target_map)

X = df_encoded.drop(columns=["Nivel_Risco", "Nivel_Risco_Num"])
y = df_encoded["Nivel_Risco_Num"]

# Dividir treino/teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Padronizar
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Treinar Random Forest (melhor modelo)
rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
rf_model.fit(X_train_scaled, y_train)

# Treinar Decision Tree (para comparação)
dt_model = DecisionTreeClassifier(max_depth=5, random_state=42)
dt_model.fit(X_train_scaled, y_train)

# Métricas rápidas
acc_rf = rf_model.score(X_test_scaled, y_test)
acc_dt = dt_model.score(X_test_scaled, y_test)
print(f"Acurácia Random Forest: {acc_rf:.4f}")
print(f"Acurácia Decision Tree: {acc_dt:.4f}")

# Salvar modelos
os.makedirs("modelos_salvos", exist_ok=True)
joblib.dump(rf_model, "modelos_salvos/spacerisk_rf_model.joblib")
joblib.dump(dt_model, "modelos_salvos/spacerisk_dt_model.joblib")
joblib.dump(scaler, "modelos_salvos/spacerisk_scaler.joblib")
joblib.dump(encoders, "modelos_salvos/spacerisk_encoders.joblib")

print("Todos os modelos e pré-processadores foram exportados para a pasta 'modelos_salvos'.")
