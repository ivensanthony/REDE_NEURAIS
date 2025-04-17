import streamlit as st
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Diagnóstico de Gripe - Rede Bayesiana", page_icon="🤧")
st.title("🤧 Diagnóstico de Gripe com Redes Bayesianas")
st.markdown("Preencha os sintomas abaixo para obter uma probabilidade de estar gripado:")

# Entrada do usuário
febre = st.selectbox("Está com febre?", ["Não", "Sim"])
dor = st.selectbox("Está com dor de cabeça?", ["Não", "Sim"])
fadiga = st.selectbox("Está com fadiga?", ["Não", "Sim"])
tosse = st.selectbox("Está com tosse?", ["Não", "Sim"])

# Modelo Bayesiano
model = DiscreteBayesianNetwork([
    ('Gripe', 'Febre'),
    ('Gripe', 'Dor'),
    ('Gripe', 'Fadiga'),
    ('Gripe', 'Tosse')
])

# CPDs
cpd_gripe = TabularCPD('Gripe', 2, [[0.6], [0.4]])

cpd_febre = TabularCPD('Febre', 2, [[0.8, 0.3], [0.2, 0.7]], evidence=['Gripe'], evidence_card=[2])
cpd_dor = TabularCPD('Dor', 2, [[0.7, 0.4], [0.3, 0.6]], evidence=['Gripe'], evidence_card=[2])
cpd_fadiga = TabularCPD('Fadiga', 2, [[0.6, 0.2], [0.4, 0.8]], evidence=['Gripe'], evidence_card=[2])
cpd_tosse = TabularCPD('Tosse', 2, [[0.9, 0.4], [0.1, 0.6]], evidence=['Gripe'], evidence_card=[2])

model.add_cpds(cpd_gripe, cpd_febre, cpd_dor, cpd_fadiga, cpd_tosse)

# Inferência
if not model.check_model():
    st.error("Erro na rede bayesiana.")
else:
    infer = VariableElimination(model)
    evidencias = {
        'Febre': 1 if febre == "Sim" else 0,
        'Dor': 1 if dor == "Sim" else 0,
        'Fadiga': 1 if fadiga == "Sim" else 0,
        'Tosse': 1 if tosse == "Sim" else 0
    }
    resultado = infer.query(variables=['Gripe'], evidence=evidencias)

    prob_nao_gripado = round(resultado.values[0] * 100, 2)
    prob_gripado = round(resultado.values[1] * 100, 2)

    # Resultado
    st.subheader("🔍 Resultado do Diagnóstico:")
    st.write(f"- **Probabilidade de NÃO estar gripado:** {prob_nao_gripado}%")
    st.write(f"- **Probabilidade de estar GRIPADO:** {prob_gripado}%")

    if prob_gripado > 70:
        st.error("⚠️ Alta chance de estar gripado! Procure atendimento médico.")
    elif prob_gripado > 40:
        st.warning("🟠 Possível gripe detectada. Fique atento aos sintomas.")
    else:
        st.success("🟢 Provavelmente não está gripado.")

    # Gráfico horizontal
    st.subheader("📊 Visualização das Probabilidades")
    fig, ax = plt.subplots(figsize=(6, 3.5))
    categorias = ['Gripado', 'Não Gripado']
    valores = [prob_gripado, prob_nao_gripado]
    cores = ['red', 'green']

    bars = ax.barh(categorias, valores, color=cores)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Probabilidade (%)")
    ax.set_title("Diagnóstico de Gripe")

    for bar in bars:
        largura = bar.get_width()
        ax.text(largura + 1, bar.get_y() + bar.get_height()/2,
                f'{largura:.1f}%', va='center', fontweight='bold')

    st.pyplot(fig)