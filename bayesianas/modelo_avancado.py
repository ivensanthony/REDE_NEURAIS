from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import matplotlib.pyplot as plt

# Estrutura da rede
modelo = DiscreteBayesianNetwork([
    ('Chuva', 'Umidade'),
    ('Irrigacao', 'Umidade'),
    ('Temperatura', 'Umidade'),
    ('Umidade', 'CrescimentoPlanta'),
    ('Sol', 'CrescimentoPlanta'),
    ('Vento', 'CrescimentoPlanta')
])

# Definindo CPDs
cpd_chuva = TabularCPD(variable='Chuva', variable_card=2, values=[[0.7], [0.3]])  # P(Chuva)
cpd_irrigacao = TabularCPD(variable='Irrigacao', variable_card=2, values=[[0.6], [0.4]])  # P(Irrigacao)
cpd_sol = TabularCPD(variable='Sol', variable_card=2, values=[[0.8], [0.2]])  # P(Sol)
cpd_temperatura = TabularCPD(variable='Temperatura', variable_card=2, values=[[0.5], [0.5]])  # P(Temperatura)
cpd_vento = TabularCPD(variable='Vento', variable_card=2, values=[[0.6], [0.4]])  # P(Vento)

cpd_umidade = TabularCPD(
    variable='Umidade', variable_card=2,
    values=[
        [0.9, 0.7, 0.4, 0.2, 0.8, 0.6, 0.3, 0.1],  # P(Umidade=0)
        [0.1, 0.3, 0.6, 0.8, 0.2, 0.4, 0.7, 0.9]   # P(Umidade=1)
    ],
    evidence=['Chuva', 'Irrigacao', 'Temperatura'],
    evidence_card=[2, 2, 2]
)

cpd_crescimento = TabularCPD(
    variable='CrescimentoPlanta', variable_card=2,
    values=[
        [0.8, 0.5, 0.4, 0.1, 0.7, 0.4, 0.3, 0.2],  # P(CrescimentoPlanta=0)
        [0.2, 0.5, 0.6, 0.9, 0.3, 0.6, 0.7, 0.8]   # P(CrescimentoPlanta=1)
    ],
    evidence=['Umidade', 'Sol', 'Vento'],
    evidence_card=[2, 2, 2]
)

# Adicionando CPDs ao modelo
modelo.add_cpds(cpd_chuva, cpd_irrigacao, cpd_sol, cpd_temperatura, cpd_vento, cpd_umidade, cpd_crescimento)

# Verificando o modelo
if modelo.check_model():
    print("O modelo está consistente!")

# Inferência
inferencia = VariableElimination(modelo)

# Consultando a probabilidade de crescimento da planta dado que houve chuva e irrigação
resultado = inferencia.query(variables=['CrescimentoPlanta'], evidence={'Chuva': 1, 'Irrigacao': 1})
print("Probabilidade de Crescimento da Planta dado Chuva e Irrigação:")
print(resultado)

# Consultando a probabilidade de umidade dado que não houve chuva
resultado_umidade = inferencia.query(variables=['Umidade'], evidence={'Chuva': 0})
print("\nProbabilidade de Umidade dado que não houve Chuva:")
print(resultado_umidade)

# Adicionando a probabilidade de Umidade ao gráfico
prob_umidade = resultado_umidade.values.tolist()  # Convertendo para lista

# Visualização gráfica das probabilidades
variaveis = ['Chuva', 'Irrigacao', 'Sol', 'Temperatura', 'Vento', 'Umidade']
probabilidades = {
    'Chuva': [0.7, 0.3],  # P(Chuva=0), P(Chuva=1)
    'Irrigacao': [0.6, 0.4],  # P(Irrigacao=0), P(Irrigacao=1)
    'Sol': [0.8, 0.2],  # P(Sol=0), P(Sol=1)
    'Temperatura': [0.5, 0.5],  # P(Temperatura=0), P(Temperatura=1)
    'Vento': [0.6, 0.4],  # P(Vento=0), P(Vento=1)
    'Umidade': prob_umidade  # P(Umidade=0), P(Umidade=1)
}

# Criar subplots em uma grade 3x2
fig, axes = plt.subplots(3, 2, figsize=(12, 12), sharey=True)

for i, var in enumerate(variaveis):
    ax = axes[i // 2, i % 2]  # Organizar em 3 linhas e 2 colunas
    bars = ax.bar([0, 1], probabilidades[var], color=['skyblue', 'orange'], tick_label=[f'{var}=0', f'{var}=1'])
    ax.set_title(f'Probabilidade de {var}')
    ax.set_ylim(0, 1)
    ax.set_ylabel('Probabilidade')
    
    # Adicionando os valores das probabilidades acima das barras
    for bar, prob in zip(bars, probabilidades[var]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02, f'{prob:.2f}', ha='center', fontsize=10)

plt.tight_layout()
plt.show()