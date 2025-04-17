import streamlit as st
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
import pandas as pd

st.set_page_config(page_title="Diagnóstico Médico", page_icon="🧠")
st.title("🩺 Diagnóstico Médico com Inteligência Artificial")

# Dados simulados
X = np.array([
    [36.5, 0, 0],
    [38.7, 1, 1],
    [37.2, 0, 0],
    [39.5, 1, 1],
    [37.8, 1, 0],
    [40.0, 1, 1],
    [36.9, 0, 0],
    [39.0, 1, 1]
])
y = np.array([0, 1, 0, 1, 1, 1, 0, 1])  # 0 = Saudável, 1 = Doente

# Treinamento
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Normalizar os dados
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

clf = MLPClassifier(hidden_layer_sizes=(5,), max_iter=1000, random_state=42)
clf.fit(X_train, y_train)

# Entradas
st.markdown("Preencha os sintomas abaixo:")
temperatura = st.slider("Temperatura Corporal (°C)", 35.0, 41.0, 36.5, 0.1)
dor_de_cabeca = st.selectbox("Dor de cabeça?", ["Não", "Sim"])
fadiga = st.selectbox("Fadiga?", ["Não", "Sim"])

entrada = np.array([[temperatura, int(dor_de_cabeca == "Sim"), int(fadiga == "Sim")]])
entrada = scaler.transform(entrada)
predicao_modelo = clf.predict(entrada)[0]
proba = clf.predict_proba(entrada)[0]

# Classificações médicas reais
def classificar_temperatura(temp):
    if temp < 35.4:
        return "Hipotermia"
    elif 35.4 <= temp <= 37.4:
        return "Normal"
    elif 37.5 <= temp <= 37.8:
        return "Febrícula"
    elif 37.9 <= temp <= 39.0:
        return "Febre"
    else:
        return "Febre Alta"

def classificar_gravidade(temp, dor, fadiga):
    if temp < 37.5 and not dor and not fadiga:
        return "Saudável"
    elif 37.5 <= temp < 38.0:
        return "Doença Leve"
    elif 38.0 <= temp <= 39.0 and dor and fadiga:
        return "Doença Moderada"
    elif temp > 39.0 and dor and fadiga:
        return "Doença Grave"
    else:
        return "Doença Leve"

nivel_temp = classificar_temperatura(temperatura)
gravidade = classificar_gravidade(temperatura, dor_de_cabeca == "Sim", fadiga == "Sim")

# Decisão final com lógica reforçada
if gravidade != "Saudável":
    predicao_final = 1  
else:
    predicao_final = predicao_modelo  

# Resultado
st.subheader("🔬 Resultado do Diagnóstico:")
if predicao_final == 0:
    st.success("**Diagnóstico Previsto: Saudável**")
    st.write("✅ Nenhum sinal grave detectado.")
else:
    st.error("**Diagnóstico Previsto: Doente**")
    st.write(f"🩺 Gravidade da condição: **{gravidade}**")
    if gravidade == "Doença Grave":
        st.warning("⚠️ **Comunicado Importante:** Procure um médico imediatamente para avaliação e tratamento adequado.")
        
        # Possíveis causas de Doença Grave
        st.write("### Possíveis causas para Doença Grave:")
        st.write("- **Infecções graves**: Pneumonia, meningite, septicemia.")
        st.write("- **Doenças inflamatórias**: Febre reumática, doença de Kawasaki.")
        st.write("- **Condições metabólicas**: Crise tireotóxica, desidratação severa.")
        st.write("- **Outras causas**: Choque séptico, complicações de doenças crônicas.")

# Motivos
st.write("### Motivos para o diagnóstico:")
st.write(f"- **Temperatura Corporal:** {temperatura:.1f} °C ({nivel_temp})")
if dor_de_cabeca == "Sim":
    st.write("- **Dor de Cabeça:** Presente")
else:
    st.write("- **Dor de Cabeça:** Ausente")
if fadiga == "Sim":
    st.write("- **Fadiga:** Presente")
else:
    st.write("- **Fadiga:** Ausente")

# Probabilidade
st.write("### Probabilidades do Modelo:")
if hasattr(clf, "predict_proba"):
    proba = clf.predict_proba(entrada)[0]
    st.write(f"- Saudável: {proba[0] * 100:.1f}%")
    st.write(f"- Doente: {proba[1] * 100:.1f}%")
else:
    st.warning("O modelo não suporta cálculo de probabilidades.")

# Avaliação
y_pred = clf.predict(X_test)
acuracia = np.mean(y_pred == y_test) * 100

# Gerar a matriz de confusão com todas as classes
cm = confusion_matrix(y_test, y_pred, labels=[0, 1])  # 0 = Saudável, 1 = Doente
labels = ["Saudável", "Doente"]

# Exibir a matriz de confusão
st.subheader("📊 Avaliação do Modelo")
st.write("### Matriz de Confusão:")
st.dataframe(pd.DataFrame(cm, index=labels, columns=labels))

# Exibir a acurácia
st.write(f"- **Acurácia:** {acuracia:.2f}%")
