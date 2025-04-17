import numpy as np
import streamlit as st
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import pandas as pd
import altair as alt
import time

# Configuração do Streamlit
st.set_page_config(page_title="🌱 Rede Bayesiana - Análise Ambiental", layout="wide")
st.title("🌿 Rede Bayesiana para Crescimento de Plantas")
st.markdown("Explore como fatores ambientais influenciam o crescimento das plantas com inferência bayesiana.")

# Estrutura da Rede Bayesiana
modelo = DiscreteBayesianNetwork([
    ('Chuva', 'Umidade'),
    ('Irrigacao', 'Umidade'),
    ('Temperatura', 'Umidade'),
    ('Umidade', 'CrescimentoPlanta'),
    ('Sol', 'CrescimentoPlanta'),
    ('Vento', 'CrescimentoPlanta')
])

# CPDs
cpd_chuva = TabularCPD('Chuva', 2, [[0.7], [0.3]])
cpd_irrigacao = TabularCPD('Irrigacao', 2, [[0.6], [0.4]])
cpd_sol = TabularCPD('Sol', 2, [[0.8], [0.2]])
cpd_temperatura = TabularCPD('Temperatura', 2, [[0.5], [0.5]])
cpd_vento = TabularCPD('Vento', 2, [[0.6], [0.4]])

cpd_umidade = TabularCPD(
    'Umidade', 2,
    [[0.9, 0.7, 0.6, 0.4, 0.8, 0.6, 0.5, 0.3],
     [0.1, 0.3, 0.4, 0.6, 0.2, 0.4, 0.5, 0.7]],
    evidence=['Chuva', 'Irrigacao', 'Temperatura'],
    evidence_card=[2, 2, 2]
)

cpd_crescimento = TabularCPD(
    'CrescimentoPlanta', 2,
    [[0.9, 0.6, 0.5, 0.3, 0.6, 0.4, 0.2, 0.1],
     [0.1, 0.4, 0.5, 0.7, 0.4, 0.6, 0.8, 0.9]],
    evidence=['Umidade', 'Sol', 'Vento'],
    evidence_card=[2, 2, 2]
)

modelo.add_cpds(cpd_chuva, cpd_irrigacao, cpd_sol, cpd_temperatura, cpd_vento, cpd_umidade, cpd_crescimento)

try:
    if modelo.check_model():
        st.success("✅ O modelo está consistente!")
except ValueError as e:
    st.error(f"❌ Erro ao verificar o modelo: {e}")

inferencia = VariableElimination(modelo)

# Interface lateral
st.sidebar.header("🔧 Configurações")
chuva_input = st.sidebar.radio("Chuva", [0, 1], format_func=lambda x: "Não" if x == 0 else "Sim")
irrigacao_input = st.sidebar.radio("Irrigação", [0, 1], format_func=lambda x: "Não" if x == 0 else "Sim")
temperatura_input = st.sidebar.radio("Temperatura", [0, 1], format_func=lambda x: "Fria" if x == 0 else "Quente")
sol_input = st.sidebar.radio("Sol", [0, 1], format_func=lambda x: "Nublado" if x == 0 else "Ensolarado")
vento_input = st.sidebar.radio("Vento", [0, 1], format_func=lambda x: "Fraco" if x == 0 else "Forte")

# Inferência
try:
    resultado_umidade = inferencia.query(
        variables=['Umidade'],
        evidence={
            'Chuva': chuva_input,
            'Irrigacao': irrigacao_input,
            'Temperatura': temperatura_input
        }
    )
    resultado_crescimento = inferencia.query(
        variables=['CrescimentoPlanta'],
        evidence={
            'Chuva': chuva_input,
            'Irrigacao': irrigacao_input,
            'Temperatura': temperatura_input,
            'Sol': sol_input,
            'Vento': vento_input
        }
    )

    prob_umidade = resultado_umidade.values[1] * 100
    prob_crescimento = resultado_crescimento.values[1] * 100

    st.subheader("🌡️ Resultados da Inferência")
    st.metric("Probabilidade de Umidade Alta", f"{prob_umidade:.2f}%")
    st.metric("Probabilidade de Crescimento da Planta", f"{prob_crescimento:.2f}%")

    # Novo gráfico de barras com Altair (sem categorias no eixo X)
    st.markdown("### 📊 Probabilidades Atuais")
    df_prob = pd.DataFrame({
        'Categoria': ['Umidade Alta', 'Crescimento da Planta'],
        'Probabilidade (%)': [prob_umidade, prob_crescimento]
    })

    df_prob['Categoria'] = df_prob['Categoria'].astype(str)
    df_prob['Probabilidade (%)'] = df_prob['Probabilidade (%)'].astype(float)

    chart = alt.Chart(df_prob).mark_bar().encode(
        x=alt.X('Categoria:N', title='Categoria', axis=alt.Axis(labels=False)),  # Remove os rótulos do eixo X
        y=alt.Y('Probabilidade (%):Q', title='Probabilidade (%)'),
        color='Categoria:N'
    ).properties(
        width=600,
        height=400,
        title="Probabilidades de Umidade e Crescimento da Planta"
    )
    st.altair_chart(chart, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao calcular as probabilidades: {e}")

# Crescimento ao longo do tempo
st.markdown("### 📈 Crescimento da Planta ao Longo do Tempo")
data = pd.DataFrame(columns=["Tempo", "Crescimento da Planta"])
chart_area = st.line_chart(data)

for i in range(100):
    novo_chuva = np.random.randint(0, 2)
    novo_irrigacao = np.random.randint(0, 2)
    novo_temperatura = np.random.randint(0, 2)
    novo_sol = np.random.randint(0, 2)
    novo_vento = np.random.randint(0, 2)

    resultado = inferencia.query(
        variables=['CrescimentoPlanta'],
        evidence={
            'Chuva': novo_chuva,
            'Irrigacao': novo_irrigacao,
            'Temperatura': novo_temperatura,
            'Sol': novo_sol,
            'Vento': novo_vento
        }
    )

    crescimento = resultado.values[1] * 100
    novo_dado = pd.DataFrame({"Tempo": [i], "Crescimento da Planta": [crescimento]})
    data = pd.concat([data, novo_dado], ignore_index=True)
    chart_area.add_rows(novo_dado)
    time.sleep(0.05)
