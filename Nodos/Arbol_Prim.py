import matplotlib.pyplot as plt
import networkx as nx

def prim(w, n, s): # pesos, numero de nodos, nodo inicial
    v = []
    while(len(v) != n):
        v.append(0)
    v[s] = 1
    E = []
    suma = 0
    for i in range(0, n-1):
        minimo = 1000
        agregar_vertice = 0
        e = []
        for j in range(0, n):
            if v[j] == 1:
                for k in range(0, n):
                    if v[k] == 0 and w[j][k] < minimo:
                        agregar_vertice = k
                        e = [j, k]
                        minimo = w[j][k]
        suma += w[e[0]][e[1]]
        v[agregar_vertice] = 1
        E.append(e)
    
    E2 = []
    for i in E:
        E2.append((i[0] + 1, i[1] + 1))
    
    return E, E2, suma

n = 6 # Número de nodos
s = 1 # Nodo inicial 

# Matriz de pesos
w = [ 
    [0, 1, 5, 7, 9, 11],  # 1 (Indice 0)
    [1, 0, 6, 4, 3, 11],  # 2 (Indice 1)
    [5, 6, 0, 5, 11, 10], # 3 (Indice 2)
    [7, 4, 5, 0, 8, 3],   # 4 (Indice 3)
    [9, 3, 11, 8, 0, 11], # 5 (Indice 4)
    [11, 11, 10, 3, 11, 0]# 6 (Indice 5)
]

E_indices_0, E_indices_1, Peso = prim(w, n, s)

print("Arbol de expansión mínima (Pares de nodos):", E_indices_1)
print("Peso Total:", Peso)

# --- PARTE GRÁFICA ---

def graficar_prim(matriz_w, aristas_mst):
    G = nx.Graph()
    nodos = range(len(matriz_w))
    
    mapping = {i: i+1 for i in nodos} 
    
    for i in range(len(matriz_w)):
        for j in range(i + 1, len(matriz_w)): 
            if matriz_w[i][j] > 0 and matriz_w[i][j] < 999: 
                G.add_edge(i, j, weight=matriz_w[i][j])


    pos = nx.spring_layout(G, seed=42) # Seed fija para que no se mueva
    
    plt.figure(figsize=(10, 7))
    
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.3, edge_color='gray', style='dashed')
    nx.draw_networkx_labels(G, pos, labels=mapping, font_size=12, font_family="sans-serif")
    

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    

    mst_edges = [(u, v) for u, v in aristas_mst]
    
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges, width=3, edge_color='red')
    
    plt.title(f"Algoritmo de Prim - Peso Total: {Peso}")
    plt.axis('off')
    plt.show()

graficar_prim(w, E_indices_0)