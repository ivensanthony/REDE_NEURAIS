import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Variáveis de entrada
temperatura = ctrl.Antecedent(np.arange(0, 41, 1), 'temperatura')
umidade = ctrl.Antecedent(np.arange(0, 101, 1), 'umidade')
velocidade_ventilador = ctrl.Consequent(np.arange(0, 101, 1), 'velocidade_ventilador')

# Funções de pertinência
temperatura['frio'] = fuzz.trimf(temperatura.universe, [0, 0, 20])  # Triangular
temperatura['médio'] = fuzz.gaussmf(temperatura.universe, 25, 5)    # Gaussiana
temperatura['quente'] = fuzz.trapmf(temperatura.universe, [30, 35, 40, 40])  # Trapezoidal

umidade['seca'] = fuzz.trimf(umidade.universe, [0, 0, 50])  # Triangular
umidade['úmida'] = fuzz.trapmf(umidade.universe, [25, 50, 75, 100])  # Trapezoidal

velocidade_ventilador['baixa'] = fuzz.trimf(velocidade_ventilador.universe, [0, 0, 50])  # Triangular
velocidade_ventilador['alta'] = fuzz.gaussmf(velocidade_ventilador.universe, 75, 10)  # Gaussiana

# Visualizar funções de pertinência
fig, axs = plt.subplots(3, 1, figsize=(8, 12))

# Gráfico para temperatura
axs[0].plot(temperatura.universe, temperatura['frio'].mf, label='Frio', color='blue')
axs[0].plot(temperatura.universe, temperatura['médio'].mf, label='Médio', color='green')
axs[0].plot(temperatura.universe, temperatura['quente'].mf, label='Quente', color='red')
axs[0].set_title('Funções de Pertinência - Temperatura')
axs[0].set_xlabel('Temperatura (°C)')
axs[0].set_ylabel('Grau de Pertinência')
axs[0].legend()

# Gráfico para umidade
axs[1].plot(umidade.universe, umidade['seca'].mf, label='Seca', color='orange')
axs[1].plot(umidade.universe, umidade['úmida'].mf, label='Úmida', color='purple')
axs[1].set_title('Funções de Pertinência - Umidade')
axs[1].set_xlabel('Umidade (%)')
axs[1].set_ylabel('Grau de Pertinência')
axs[1].legend()

# Gráfico para velocidade do ventilador
axs[2].plot(velocidade_ventilador.universe, velocidade_ventilador['baixa'].mf, label='Baixa', color='cyan')
axs[2].plot(velocidade_ventilador.universe, velocidade_ventilador['alta'].mf, label='Alta', color='magenta')
axs[2].set_title('Funções de Pertinência - Velocidade do Ventilador')
axs[2].set_xlabel('Velocidade (%)')
axs[2].set_ylabel('Grau de Pertinência')
axs[2].legend()

plt.tight_layout()
plt.show()