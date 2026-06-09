import os
import numpy as np
import pandas as pd

# Definir semente aleatória para reprodutibilidade
np.random.seed(42)

# Número de amostras
n_samples = 3000

# Estados e Biomas brasileiros representativos com coordenadas centrais aproximadas
estados_coords = {
    "SP": (-23.55, -46.63),
    "MG": (-18.51, -44.55),
    "AM": (-3.47, -62.22),
    "MT": (-12.68, -56.92),
    "BA": (-12.58, -41.70),
    "RS": (-30.03, -51.23),
    "GO": (-15.83, -49.84),
    "PA": (-5.54, -52.73),
    "CE": (-5.10, -39.65),
    "PR": (-24.89, -51.55)
}

estados_biomas = [
    ("SP", "Mata Atlântica"), ("MG", "Cerrado"), ("AM", "Amazônia"),
    ("MT", "Cerrado/Amazônia"), ("BA", "Caatinga"), ("RS", "Pampa"),
    ("GO", "Cerrado"), ("PA", "Amazônia"), ("CE", "Caatinga"), ("PR", "Mata Atlântica")
]

# Escolhas aleatórias de estado e bioma
indices_estados = np.random.choice(len(estados_biomas), n_samples)
estados = [estados_biomas[i][0] for i in indices_estados]
biomas = [estados_biomas[i][1] for i in indices_estados]

# Gerar latitude e longitude baseadas no estado com um ruído para simular cidades diferentes
latitudes = []
longitudes = []
for est in estados:
    base_lat, base_lon = estados_coords[est]
    lat = base_lat + np.random.normal(0, 1.5) # Desvio padrão de ~160km
    lon = base_lon + np.random.normal(0, 1.5)
    latitudes.append(lat)
    longitudes.append(lon)

# Meses de coleta de dados
meses = np.random.choice([
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
], n_samples)

# Variáveis Climáticas e de Sensoriamento Remoto
temperatura = np.random.uniform(15.0, 42.0, n_samples)
umidade = np.random.uniform(10.0, 95.0, n_samples)
precipitacao = np.random.exponential(scale=120.0, size=n_samples)
precipitacao = np.minimum(precipitacao, 500.0) # teto
ndvi = np.random.uniform(-0.1, 0.9, n_samples)
focos_calor = np.random.negative_binomial(n=2, p=0.05, size=n_samples)
declividade = np.random.uniform(0.0, 40.0, n_samples)
distancia_rios = np.random.uniform(10.0, 5000.0, n_samples)

usos_solo = ["Floresta", "Cerrado/Savana", "Pastagem", "Agricultura", "Área Urbana", "Corpo d'Água"]
uso_solo = np.random.choice(usos_solo, n_samples, p=[0.3, 0.2, 0.2, 0.15, 0.1, 0.05])

# Ajustes lógicos nas variáveis
for i in range(n_samples):
    if uso_solo[i] == "Corpo d'Água":
        ndvi[i] = np.random.uniform(-0.2, 0.1)
        umidade[i] = np.random.uniform(70.0, 98.0)
        focos_calor[i] = 0
        distancia_rios[i] = np.random.uniform(0.0, 50.0)
    elif uso_solo[i] == "Floresta":
        ndvi[i] = np.random.uniform(0.6, 0.9)
    
    if temperatura[i] > 35.0 and umidade[i] < 30.0:
        focos_calor[i] += np.random.randint(10, 50)
        ndvi[i] = np.maximum(ndvi[i] - 0.2, -0.1)

# Cálculo de risco composto
risco_queimada = (
    (temperatura - 25.0) * 1.5 + 
    (70.0 - umidade) * 1.2 - 
    precipitacao * 0.4 + 
    (0.5 - ndvi) * 15.0 + 
    focos_calor * 0.8
)

risco_enchente_deslizamento = (
    precipitacao * 1.2 + 
    declividade * 1.8 - 
    (distancia_rios / 100.0) * 2.0
)

for i in range(n_samples):
    if uso_solo[i] == "Área Urbana":
        risco_enchente_deslizamento[i] += 50.0
    elif uso_solo[i] == "Corpo d'Água":
        risco_queimada[i] = -100.0

risco_composto = np.maximum(risco_queimada, risco_enchente_deslizamento)
ruido = np.random.normal(0, 15, n_samples)
risco_final = risco_composto + ruido

# Thresholds para classificação
q25 = np.percentile(risco_final, 35)
q75 = np.percentile(risco_final, 75)

nivel_risco = []
for r in risco_final:
    if r < q25:
        nivel_risco.append("Baixo")
    elif r < q75:
        nivel_risco.append("Médio")
    else:
        nivel_risco.append("Alto")

# Criar DataFrame
df = pd.DataFrame({
    "Estado": estados,
    "Bioma": biomas,
    "Latitude": np.round(latitudes, 5),
    "Longitude": np.round(longitudes, 5),
    "Mês": meses,
    "Temperatura": np.round(temperatura, 1),
    "Umidade": np.round(umidade, 1),
    "Precipitacao": np.round(precipitacao, 1),
    "NDVI": np.round(ndvi, 3),
    "Focos_Calor": focos_calor,
    "Declividade": np.round(declividade, 1),
    "Distancia_Rios": np.round(distancia_rios, 1),
    "Uso_Solo": uso_solo,
    "Nivel_Risco": nivel_risco
})

# Salvar o CSV
os.makedirs("data", exist_ok=True)
output_path = "data/dados_ambientais.csv"
df.to_csv(output_path, index=False)
print(f"Dataset com coordenadas gerado com sucesso em '{output_path}' com {len(df)} amostras.")
