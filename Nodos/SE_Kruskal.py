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


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank   = [0] * n

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        ri, rj = self.find(i), self.find(j)
        if ri == rj:
            return False
        if self.rank[ri] > self.rank[rj]:
            self.parent[rj] = ri
        else:
            self.parent[ri] = rj
            if self.rank[ri] == self.rank[rj]:
                self.rank[rj] += 1
        return True


def kruskal(w, n, buscar_maximo=False):

    aristas = [
        [i, j, w[i][j]]
        for i in range(n)
        for j in range(i + 1, n)
        if w[i][j] != 0
    ]
    aristas.sort(key=lambda x: x[2], reverse=buscar_maximo)

    uf = UnionFind(n)
    mst_aristas = []
    mst_peso    = 0

    print("\nOrden de evaluación de aristas:")
    for u, v, peso in aristas:
        aceptada = uf.union(u, v)
        estado   = "✔ ACEPTADA" if aceptada else "✘ Rechazada (ciclo)"
        print(f"  {MUNICIPIOS[u]:15s} — {MUNICIPIOS[v]:15s}  "
              f"costo={peso:>3}  {estado}")
        if aceptada:
            mst_aristas.append([u, v])
            mst_peso += peso

    aristas_nombres = [(MUNICIPIOS[u], MUNICIPIOS[v]) for u, v in mst_aristas]
    return mst_aristas, aristas_nombres, mst_peso


def graficar_kruskal(matriz_w, aristas_mst, peso_total, tipo):
    G = nx.Graph()
    n = len(matriz_w)

    for i in range(n):
        for j in range(i + 1, n):
            if 0 < matriz_w[i][j] < 999:
                G.add_edge(i, j, weight=matriz_w[i][j])

    pos   = nx.spring_layout(G, seed=7)
    color = 'mediumblue' if tipo == 'Mínimo' else 'darkorange'

    plt.figure(figsize=(11, 7))
    nx.draw_networkx_nodes(G, pos, node_size=800, node_color='#A9DFBF')
    nx.draw_networkx_edges(G, pos, width=1.2, alpha=0.25,
                           edge_color='gray', style='dashed')
    nx.draw_networkx_labels(G, pos, labels=MUNICIPIOS, font_size=9,
                            font_weight='bold')
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'),
        font_size=8, label_pos=0.3
    )

    mst_edges = [(u, v) for u, v in aristas_mst]
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges,
                           width=3.5, edge_color=color)

    plt.title(
        f"Kruskal — Árbol de Expansión {tipo}\n"
        f"Costo Total: ${peso_total * 10:,}K MXN  |  "
        f"Aristas resaltadas = enlaces seleccionados",
        fontsize=12
    )
    plt.axis('off')
    plt.tight_layout()
    fname = f"Nodos/Outputs/Kruskal_{tipo}_resultado.png"
    plt.savefig(fname, dpi=150)
    plt.show()
    print(f"Gráfica guardada: {fname}")


n = 6

w = [
    [0,  8,  12, 20, 25, 45],  # Guadalajara
    [8,  0,  18, 22, 15, 50],  # Zapopan
    [12, 18,  0,  6,  14, 38], # Tlaquepaque
    [20, 22,  6,  0,  10, 30], # Tonalá
    [25, 15, 14, 10,  0,  20], # Tlajomulco
    [45, 50, 38, 30, 20,  0],  # Chapala
]

modo_maximo = False
tipo = "Máximo" if modo_maximo else "Mínimo"

print("=" * 60)
print(f"  SISTEMA EXPERTO — RED DE FIBRA ÓPTICA (KRUSKAL {tipo.upper()})")
print("=" * 60)

aristas_idx, aristas_nombres, costo = kruskal(w, n, buscar_maximo=modo_maximo)

print(f"\nArbol de Expansión {tipo}:")
for origen, destino in aristas_nombres:
    print(f"   {origen:15s} ──── {destino}")
print(f"\nCosto total: ${costo * 10:,}K MXN")

if modo_maximo:
    print("\nModo MÁXIMO: muestra el peor escenario de inversión.")
else:
    print("\nModo MÍNIMO: configuración óptima para minimizar inversión.")

graficar_kruskal(w, aristas_idx, costo, tipo)