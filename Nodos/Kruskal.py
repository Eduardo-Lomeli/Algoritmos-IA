import matplotlib.pyplot as plt
import networkx as nx

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            if self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_i] = root_j
                if self.rank[root_i] == self.rank[root_j]:
                    self.rank[root_j] += 1
            return True
        return False

def kruskal(w, n, buscar_maximo=False):
    # 1. Crear lista de aristas
    aristas = []
    for i in range(n):
        for j in range(i + 1, n):
            if w[i][j] != 0:
                aristas.append([i, j, w[i][j]])
    # 2. Ordenar aristas
    aristas.sort(key=lambda x: x[2], reverse=buscar_maximo)
    
    uf = UnionFind(n)
    mst_aristas = []
    mst_peso = 0
    
    # 3. Iterar y seleccionar
    for u, v, peso in aristas:
        if uf.union(u, v):
            mst_aristas.append([u, v])
            mst_peso += peso
            
    mst_aristas_print = [(u + 1, v + 1) for u, v in mst_aristas]
    
    return mst_aristas, mst_aristas_print, mst_peso

n = 6
w = [ 
    [0, 1, 5, 7, 9, 11],
    [1, 0, 6, 4, 3, 11],
    [5, 6, 0, 5, 11, 10],
    [7, 4, 5, 0, 8, 3],
    [9, 3, 11, 8, 0, 11],
    [11, 11, 10, 3, 11, 0]
]

modo_maximo = False 
E_indices, E_print, Peso = kruskal(w, n, buscar_maximo=modo_maximo)

tipo_arbol = "Máximo" if modo_maximo else "Mínimo"
print(f"Árbol de expansión {tipo_arbol} (Kruskal):", E_print)
print("Peso Total:", Peso)


def graficar_kruskal(matriz_w, aristas_mst, peso_total, titulo_tipo):
    G = nx.Graph()
    nodos = range(len(matriz_w))
    mapping = {i: i+1 for i in nodos} 
    
    for i in range(len(matriz_w)):
        for j in range(i + 1, len(matriz_w)):
            if matriz_w[i][j] > 0 and matriz_w[i][j] < 999:
                G.add_edge(i, j, weight=matriz_w[i][j])

    pos = nx.spring_layout(G, seed=42)
    
    plt.figure(figsize=(10, 7))
    
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightgreen') 
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.3, edge_color='gray', style='dashed')
    nx.draw_networkx_labels(G, pos, labels=mapping, font_size=12)
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
 
    mst_edges_tuples = [(u, v) for u, v in aristas_mst]
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges_tuples, width=3, edge_color='blue')
    
    plt.title(f"Algoritmo de Kruskal ({titulo_tipo}) - Peso: {peso_total}")
    plt.axis('off')
    plt.show()

graficar_kruskal(w, E_indices, Peso, tipo_arbol)