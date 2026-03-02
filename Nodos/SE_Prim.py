import matplotlib.pyplot as plt
import networkx as nx

MUNICIPIOS = {
    0: "Guadalajara",
    1: "Zapopan",
    2: "Tlaquepaque",
    3: "Tonalá",
    4: "Tlajomulco",
    5: "Chapala"
}

def prim(w, n, s):

    visitados = [0] * n
    visitados[s] = 1
    aristas_mst = []
    costo_total = 0

    for _ in range(n - 1):
        minimo = float('inf')
        nodo_destino = -1
        arista = []

        for j in range(n):
            if visitados[j] == 1:
                for k in range(n):
                    if visitados[k] == 0 and 0 < w[j][k] < minimo:
                        nodo_destino = k
                        arista = [j, k]
                        minimo = w[j][k]

        costo_total += w[arista[0]][arista[1]]
        visitados[nodo_destino] = 1
        aristas_mst.append(arista)

    aristas_nombradas = [(MUNICIPIOS[u], MUNICIPIOS[v]) for u, v in aristas_mst]
    return aristas_mst, aristas_nombradas, costo_total


def graficar_prim(matriz_w, aristas_mst, costo_total):
    G = nx.Graph()
    n = len(matriz_w)
    labels = MUNICIPIOS

    for i in range(n):
        for j in range(i + 1, n):
            if 0 < matriz_w[i][j] < 999:
                G.add_edge(i, j, weight=matriz_w[i][j])

    pos = nx.spring_layout(G, seed=7)
    plt.figure(figsize=(11, 7))

    # Grafo completo (todas las conexiones posibles, en gris)
    nx.draw_networkx_nodes(G, pos, node_size=800, node_color='#AED6F1')
    nx.draw_networkx_edges(G, pos, width=1.2, alpha=0.25,
                           edge_color='gray', style='dashed')
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=9,
                            font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                 font_size=8, label_pos=0.3)

    mst_edges = [(u, v) for u, v in aristas_mst]
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges,
                           width=3.5, edge_color='crimson')

    plt.title(
        f"Prim — Red de Fibra Optica \n",
        fontsize=12
    )
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("Nodos/Outputs/SE_Prim_resultado.png", dpi=150)
    plt.show()



n = 6 
s = 0   # Nodo inicial

# Costo de tendido de fibra optica entre municipios
w = [
    [0,  8,  12, 20, 25, 45],  # Guadalajara
    [8,  0,  18, 22, 15, 50],  # Zapopan
    [12, 18,  0,  6,  14, 38], # Tlaquepaque
    [20, 22,  6,  0,  10, 30], # Tonalá
    [25, 15, 14, 10,  0,  20], # Tlajomulco
    [45, 50, 38, 30, 20,  0],  # Chapala
]

aristas_idx, aristas_nombres, costo = prim(w, n, s)

print("=" * 55)
print("  SISTEMA EXPERTO — RED DE FIBRA ÓPTICA (PRIM)")
print("=" * 55)
print(f"\nNodo inicial: {MUNICIPIOS[s]}")
print("\nConexiones a instalar (Árbol de Expansión Mínima):")
for origen, destino in aristas_nombres:
    print(f"   {origen:15s} ──── {destino}")
print(f"\nCosto total de infraestructura: ${costo * 10:,}K MXN")
print(f"(Se ahorran conexiones redundantes tendiendo solo {len(aristas_nombres)} enlaces)")

graficar_prim(w, aristas_idx, costo)