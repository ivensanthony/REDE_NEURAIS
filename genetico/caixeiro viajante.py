import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt

# Definições do problema
CIDADES = ["A", "B", "C", "D", "E"]
DISTANCIAS = {
    ("A", "B"): 2, ("A", "C"): 5, ("A", "D"): 7, ("A", "E"): 3,
    ("B", "C"): 4, ("B", "D"): 6, ("B", "E"): 2,
    ("C", "D"): 8, ("C", "E"): 3,
    ("D", "E"): 6
}

G = nx.Graph()
for (c1, c2), dist in DISTANCIAS.items():
    G.add_edge(c1, c2, weight=dist)

def calcular_distancia(caminho):
    distancia = 0
    for i in range(len(caminho) - 1):
        par = (caminho[i], caminho[i + 1])
        if par not in DISTANCIAS:
            par = (caminho[i + 1], caminho[i]) 
        distancia += DISTANCIAS[par]
    return distancia
POP_SIZE = 10
GERACOES = 100
populacao = [random.sample(CIDADES, len(CIDADES)) for _ in range(POP_SIZE)]

for _ in range(GERACOES):
    populacao = sorted(populacao, key=calcular_distancia)

    pais = populacao[:3]

    filho = pais[0][:2] + [c for c in pais[1] if c not in pais[0][:2]]

    if random.random() < 0.2:
        i, j = random.sample(range(len(CIDADES)), 2)
        filho[i], filho[j] = filho[j], filho[i]

    populacao.append(filho)

melhor_solucao = min(populacao, key=calcular_distancia)
print(f"Melhor caminho: {melhor_solucao}, Distância: {calcular_distancia(melhor_solucao)}")


pos = nx.spring_layout(G)  
plt.figure(figsize=(8, 6))


nx.draw(G, pos, with_labels=True, node_color='orange', edge_color='gray', node_size=2000, font_size=12)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)


edges_melhor = [(melhor_solucao[i], melhor_solucao[i + 1]) for i in range(len(melhor_solucao) - 1)]
nx.draw_networkx_edges(G, pos, edgelist=edges_melhor, edge_color='red', width=2)

plt.title("Melhor Caminho Encontrado pelo Algoritmo Genético")
plt.show()
