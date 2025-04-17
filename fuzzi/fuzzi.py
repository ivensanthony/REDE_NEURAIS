import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import streamlit as st
import time

st.set_page_config(page_title="Sistema Fuzzy - Finanças", layout="centered")
st.title("💰 Sistema Fuzzy - Análise Financeira com Indicadores de Sentimento")

# Variáveis de entrada
bpi = ctrl.Antecedent(np.arange(0, 101, 1), 'bpi')
vix = ctrl.Antecedent(np.arange(0, 101, 1), 'vix')
bmi = ctrl.Antecedent(np.arange(0, 101, 1), 'bmi')
ssi = ctrl.Antecedent(np.arange(0, 101, 1), 'ssi')

# Variável de saída
sentimento_mercado = ctrl.Consequent(np.arange(0, 101, 1), 'sentimento_mercado')

# Funções de pertinência
bpi['baixo'] = fuzz.trimf(bpi.universe, [0, 0, 50])
bpi['moderado'] = fuzz.trimf(bpi.universe, [30, 50, 70])
bpi['alto'] = fuzz.trimf(bpi.universe, [50, 100, 100])

vix['baixo'] = fuzz.trimf(vix.universe, [0, 0, 20])
vix['moderado'] = fuzz.trimf(vix.universe, [15, 25, 35])
vix['alto'] = fuzz.trimf(vix.universe, [30, 100, 100])

bmi['pessimista'] = fuzz.trimf(bmi.universe, [0, 0, 27])
bmi['neutro'] = fuzz.trimf(bmi.universe, [20, 50, 67])
bmi['euforico'] = fuzz.trimf(bmi.universe, [50, 100, 100])

ssi['venda'] = fuzz.trimf(ssi.universe, [0, 0, 50])
ssi['neutro'] = fuzz.trimf(ssi.universe, [30, 50, 70])
ssi['compra'] = fuzz.trimf(ssi.universe, [50, 100, 100])

sentimento_mercado['pessimista'] = fuzz.trimf(sentimento_mercado.universe, [0, 0, 50])
sentimento_mercado['neutro'] = fuzz.trimf(sentimento_mercado.universe, [30, 50, 70])
sentimento_mercado['otimista'] = fuzz.trimf(sentimento_mercado.universe, [50, 100, 100])

# Regras Fuzzy
regras = [
    ctrl.Rule(bpi['alto'] & vix['baixo'] & bmi['euforico'] & ssi['compra'], sentimento_mercado['otimista']),
    ctrl.Rule(bpi['moderado'] & vix['moderado'] & bmi['neutro'] & ssi['neutro'], sentimento_mercado['neutro']),
    ctrl.Rule(bpi['baixo'] | vix['alto'] | bmi['pessimista'] | ssi['venda'], sentimento_mercado['pessimista']),
    ctrl.Rule(~(bpi['alto'] | bpi['moderado'] | bpi['baixo']), sentimento_mercado['neutro'])
]

sistema_controle = ctrl.ControlSystem(regras)
simulador = ctrl.ControlSystemSimulation(sistema_controle)

st.sidebar.title("Parâmetros de Entrada")
bpi_input = st.sidebar.slider("Bullish Percent Index (BPI) (%)", 0, 100, 50)
vix_input = st.sidebar.slider("Volatility Index (VIX)", 0, 100, 20)
bmi_input = st.sidebar.slider("Bitcoin Misery Index (BMI)", 0, 100, 50)
ssi_input = st.sidebar.slider("Sentiment Strength Index (SSI)", 0, 100, 50)

try:
    simulador.input['bpi'] = bpi_input
    simulador.input['vix'] = vix_input
    simulador.input['bmi'] = bmi_input
    simulador.input['ssi'] = ssi_input
    simulador.compute()

    sentimento = simulador.output['sentimento_mercado']
    st.write(f"### Sentimento do Mercado: {sentimento:.2f}%")
except KeyError as e:
    st.error(f"Erro ao calcular o sentimento do mercado: {e}")

st.write("### Gráfico em Tempo Real - Todos os Indicadores")
chart = st.line_chart()

# Gráficos separados para cada indicador com títulos
st.write("### Gráficos Separados para Cada Indicador")

st.write("#### Bullish Percent Index (BPI)")
chart_bpi = st.line_chart()

st.write("#### Volatility Index (VIX)")
chart_vix = st.line_chart()

st.write("#### Bitcoin Misery Index (BMI)")
chart_bmi = st.line_chart()

st.write("#### Sentiment Strength Index (SSI)")
chart_ssi = st.line_chart()

st.write("#### Sentimento do Mercado")
chart_sentimento = st.line_chart()

st.sidebar.write("### O que os indicadores representam:")
st.sidebar.write("- **BPI (Bullish Percent Index)**: Mede a porcentagem de ações com padrões de alta, indicando o otimismo do mercado.")
st.sidebar.write("- **VIX (Volatility Index)**: Mede a volatilidade implícita das opções financeiras. Valores baixos indicam estabilidade, enquanto valores altos indicam alta volatilidade.")
st.sidebar.write("- **BMI (Bitcoin Misery Index)**: Avalia o sentimento do mercado de Bitcoin. Valores baixos indicam pessimismo, enquanto valores altos indicam euforia.")
st.sidebar.write("- **SSI (Sentiment Strength Index)**: Mede a força do sentimento de compra/venda com base na porcentagem de compradores e vendedores.")
st.sidebar.write("- **Sentimento do Mercado**: Resultado fuzzy que indica se o mercado está pessimista, neutro ou otimista.")

for i in range(100):
    novo_bpi = np.random.randint(0, 101)
    novo_vix = np.random.randint(0, 101)
    novo_bmi = np.random.randint(0, 101)
    novo_ssi = np.random.randint(0, 101)

    simulador.input['bpi'] = novo_bpi
    simulador.input['vix'] = novo_vix
    simulador.input['bmi'] = novo_bmi
    simulador.input['ssi'] = novo_ssi
    simulador.compute()

    chart.add_rows({
        "BPI": [novo_bpi],
        "VIX": [novo_vix],
        "BMI": [novo_bmi],
        "SSI": [novo_ssi],
        "Sentimento do Mercado": [simulador.output['sentimento_mercado']]
    })

    chart_bpi.add_rows({"BPI": [novo_bpi]})
    chart_vix.add_rows({"VIX": [novo_vix]})
    chart_bmi.add_rows({"BMI": [novo_bmi]})
    chart_ssi.add_rows({"SSI": [novo_ssi]})
    chart_sentimento.add_rows({"Sentimento do Mercado": [simulador.output['sentimento_mercado']]})

    time.sleep(0.1)