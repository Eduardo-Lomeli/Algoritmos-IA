import heapq
import networkx as nx
import matplotlib.pyplot as plt
import time

class Estado:
    def __init__(self, nombre):
        self.nombre = nombre
    def __repr__(self):
        return self.nombre

class Accion:
    def __init__(self, nombre):
        self.nombre = nombre

def obtener_datos():
    lanoi = Estado("Lanoi")
    nohoi = Estado("Nohoi")
    ruun = Estado("Ruun")
    milos = Estado("Milos")
    ghiido = Estado("Ghiido")
    kuart = Estado("Kuart")
    boomon = Estado("Boomon")
    goorum = Estado("Goorum")
    shiphos = Estado("Shiphos")
    nokshos = Estado("Nokshos")
    pharis = Estado("Pharis")
    khamin = Estado("Khamin")
    tarios = Estado("Tarios")
    peranna = Estado("Peranna")
    khandan = Estado("Khandan")
    tawa = Estado("Tawa")
    theer = Estado("Theer")
    roria = Estado("Roria")
    kosos = Estado("Kosos")

    acciones_con_costo = {
        'Lanoi': {'NE': ('nohoi', 3), 'SO': ('lanoi', 1), 'NO': ('ruun', 5)},
        'Nohoi': {'NE': ('milos', 4), 'SO': ('lanoi', 3)},
        'Ruun': {'NO': ('ghiido', 6), 'NE': ('kuart', 5), 'E': ('milos', 3), 'SE': ('nohoi', 2)},
        'Milos': {'O': ('ruun', 3), 'SO': ('nohoi', 4), 'N': ('khandan', 10)},
        'Ghiido': {'N': ('nokshos', 7), 'E': ('kuart', 2), 'SE': ('ruun', 6)},
        'Kuart': {'O': ('ghiido', 2), 'SO': ('ruun', 5), 'NE': ('boomon', 3)},
        'Boomon': {'N': ('goorum', 2), 'SO': ('kuart', 3)},
        'Goorum': {'O': ('shiphos', 4), 'S': ('boomon', 2)},
        'Shiphos': {'O': ('nokshos', 5), 'E': ('goorum', 4)},
        'Nokshos': {'NO': ('pharis', 3), 'S': ('ghiido', 7), 'E': ('shiphos', 5)},
        'Pharis': {'NO': ('khamin', 4), 'SO': ('nokshos', 3)},
        'Khamin': {'SE': ('pharis', 4), 'NO': ('tawa', 6), 'O': ('tarios', 5)},
        'Tarios': {'O': ('khamin', 5), 'NO': ('tawa', 3), 'NE': ('roria', 4), 'E': ('peranna', 2)},
        'Peranna': {'O': ('tarios', 2), 'E': ('khandan', 3)},
        'Khandan': {'O': ('peranna', 3), 'S': ('milos', 10)},
        'Tawa': {'SO': ('khamin', 6), 'SE': ('tarios', 3), 'NE': ('theer', 2)},
        'Theer': {'SO': ('tawa', 2), 'SE': ('roria', 3)},
        'Roria': {'NO': ('theer', 3), 'SO': ('tarios', 4), 'E': ('kosos', 5)},
        'Kosos': {'O': ('roria', 5)}
    }
    return acciones_con_costo

def normalizar_grafo(acciones_raw):
    grafo_limpio = {}
    
    for origen, movimientos in acciones_raw.items():
        grafo_limpio[origen] = {}
        for direccion, datos in movimientos.items():
            destino_raw, costo = datos
            destino_normalizado = destino_raw.title() 
            
            grafo_limpio[origen][destino_normalizado] = costo
            
    return grafo_limpio

def ejecutar_dijkstra(grafo, inicio, fin):
    cola = [(0, inicio)]
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    padres = {nodo: None for nodo in grafo}
    visitados = set()

    print(f"\nBÚSQUEDA DE RUTA: {inicio} -> {fin}")
    print("-" * 60)

    while cola:
        costo_actual, nodo_actual = heapq.heappop(cola)

        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)

        print(f"Nodo actual: {nodo_actual} (Acumulado: {costo_actual})")

        if nodo_actual == fin:
            print(f" Llegada a {fin}! Costo final: {costo_actual}")
            break

        for vecino, peso in grafo.get(nodo_actual, {}).items():
            if vecino not in distancias: continue # Por seguridad si hay referencias rotas

            nuevo_costo = costo_actual + peso
            print(f"     Vecino: {vecino} (Arista: {peso}) -> Nuevo total: {nuevo_costo}")

            if nuevo_costo < distancias[vecino]:
                print(f"Actualizando ruta a {vecino} (Antes: {distancias[vecino]})")
                distancias[vecino] = nuevo_costo
                padres[vecino] = nodo_actual
                heapq.heappush(cola, (nuevo_costo, vecino))
        
        time.sleep(0.5)

    # Reconstruir camino
    ruta = []
    actual = fin
    while actual:
        ruta.insert(0, actual)
        actual = padres[actual]
    
    if distancias[fin] == float('inf'):
        return [], float('inf')
    return ruta, distancias[fin]

# --- 5. VISUALIZADOR GRÁFICO ---
def visualizar(grafo_dict, ruta, inicio, fin):
    G = nx.DiGraph()
    
    for origen, destinos in grafo_dict.items():
        for destino, peso in destinos.items():
            G.add_edge(origen, destino, weight=peso)

    pos = nx.kamada_kawai_layout(G) 
    
    plt.figure(figsize=(12, 8))
    
    # Dibujar todo el grafo en gris
    nx.draw_networkx_nodes(G, pos, node_color='lightgray', node_size=600)
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, alpha=0.3)
    nx.draw_networkx_labels(G, pos, font_size=9)
    
    # Etiquetas de pesos
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

    if ruta:
        # Nodos de la ruta
        nx.draw_networkx_nodes(G, pos, nodelist=ruta, node_color='#4CAF50', node_size=700)
        # Aristas de la ruta
        aristas_ruta = [(ruta[i], ruta[i+1]) for i in range(len(ruta)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=aristas_ruta, edge_color='red', width=2.5)
        
        # Marcar inicio y fin
        nx.draw_networkx_nodes(G, pos, nodelist=[inicio], node_color='gold', node_size=800, label="Inicio")
        nx.draw_networkx_nodes(G, pos, nodelist=[fin], node_color='orange', node_size=800, label="Fin")

    plt.title(f"Ruta Óptima: {' -> '.join(ruta)}", fontsize=14)
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    raw_data = obtener_datos()

    grafo_normalizado = normalizar_grafo(raw_data)
    
    # 3. Definir inicio y fin
    NODO_INICIO = 'Lanoi'
    NODO_FIN = 'Kosos'
    
    # 4. Correr Dijkstra
    camino, costo_total = ejecutar_dijkstra(grafo_normalizado, NODO_INICIO, NODO_FIN)
    
    # 5. Mostrar resultado final
    if camino:
        print(f"\nRESULTADO: La mejor ruta es: {camino} con costo {costo_total}")
        visualizar(grafo_normalizado, camino, NODO_INICIO, NODO_FIN)
    else:
        print("\nNo se encontró un camino posible.")