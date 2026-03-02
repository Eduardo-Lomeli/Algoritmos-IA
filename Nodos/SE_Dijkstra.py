import heapq
import networkx as nx
import matplotlib.pyplot as plt


RED_VIAL = {
    "Guadalajara Centro": {
        "Zapopan":           18,
        "Tlaquepaque":       22,
        "Providencia":       12,
    },
    "Zapopan": {
        "Guadalajara Centro": 20,
        "Tesistán":           25,
        "Providencia":        14,
        "El Colli":           10,
    },
    "Tlaquepaque": {
        "Guadalajara Centro": 25,
        "Tonalá":             15,
        "Tlajomulco":         30,
    },
    "Tonalá": {
        "Tlaquepaque":        16,
        "Tlajomulco":         22,
        "El Salto":           18,
    },
    "Tlajomulco": {
        "Tonalá":             22,
        "Tlaquepaque":        28,
        "Chapala":            40,
        "El Salto":           20,
    },
    "Providencia": {
        "Guadalajara Centro": 14,
        "Zapopan":            15,
        "Tesistán":           35,
    },
    "El Colli": {
        "Zapopan":            12,
        "Tesistán":           20,
    },
    "Tesistán": {
        "El Colli":           22,
        "Zapopan":            27,
        "Chapala":            55,
    },
    "El Salto": {
        "Tonalá":             19,
        "Tlajomulco":         21,
        "Chapala":            35,
    },
    "Chapala": {
        "Tlajomulco":         42,
        "El Salto":           36,
        "Ajijic":             12,
    },
    "Ajijic": {
        "Chapala":            13,
    },
}


def dijkstra(grafo: dict, inicio: str, fin: str):
    cola       = [(0, inicio)]
    distancias = {nodo: float('inf') for nodo in grafo}
    padres     = {nodo: None        for nodo in grafo}
    distancias[inicio] = 0
    visitados  = set()

    print(f"\n{'='*60}")
    print(f"  BUSCANDO RUTA: {inicio}  →  {fin}")
    print(f"{'='*60}")

    while cola:
        costo_actual, nodo_actual = heapq.heappop(cola)

        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)

        print(f"\n▶ Visitando: {nodo_actual}  (acumulado: {costo_actual} min)")

        if nodo_actual == fin:
            print(f"  ✔ ¡Destino alcanzado! Tiempo mínimo: {costo_actual} min")
            break

        for vecino, tiempo in grafo.get(nodo_actual, {}).items():
            if vecino not in distancias:
                continue
            nuevo_costo = costo_actual + tiempo
            if nuevo_costo < distancias[vecino]:
                print(f"    Actualizando {vecino}: {distancias[vecino]} → {nuevo_costo} min")
                distancias[vecino] = nuevo_costo
                padres[vecino]     = nodo_actual
                heapq.heappush(cola, (nuevo_costo, vecino))

    # Reconstruir ruta
    ruta, actual = [], fin
    while actual:
        ruta.insert(0, actual)
        actual = padres.get(actual)

    if distancias[fin] == float('inf'):
        return [], float('inf')
    return ruta, distancias[fin]


def visualizar(grafo_dict: dict, ruta: list, inicio: str, fin: str,
               costo_total: int):
    G = nx.DiGraph()
    for origen, destinos in grafo_dict.items():
        for destino, peso in destinos.items():
            G.add_edge(origen, destino, weight=peso)

    pos = nx.kamada_kawai_layout(G)
    plt.figure(figsize=(14, 9))

    # Fondo completo
    nx.draw_networkx_nodes(G, pos, node_color='#D5DBDB', node_size=700)
    nx.draw_networkx_edges(G, pos, edge_color='#BDC3C7',
                           arrows=True, alpha=0.4, arrowsize=12)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=nx.get_edge_attributes(G, 'weight'),
        font_size=7
    )

    if ruta:
        # Nodos de la ruta óptima
        nx.draw_networkx_nodes(G, pos, nodelist=ruta,
                               node_color='#27AE60', node_size=800)
        # Aristas de la ruta
        aristas_ruta = [(ruta[i], ruta[i+1]) for i in range(len(ruta) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=aristas_ruta,
                               edge_color='#E74C3C', width=3,
                               arrows=True, arrowsize=20)
        # Inicio / fin
        nx.draw_networkx_nodes(G, pos, nodelist=[inicio],
                               node_color='#F1C40F', node_size=900)
        nx.draw_networkx_nodes(G, pos, nodelist=[fin],
                               node_color='#E67E22', node_size=900)

    ruta_str = " → ".join(ruta) if ruta else "Sin ruta"
    plt.title(
        f"Dijkstra — Ruta de entrega óptima (paquetería Jalisco)\n"
        f"{ruta_str}\n"
        f"Tiempo estimado: {costo_total} minutos  |  Origen  Destino  Ruta",
        fontsize=11
    )
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("Nodos/Outputs/Dijkstra_resultado.png", dpi=150)
    plt.show()


ORIGEN  = "Zapopan"
DESTINO = "Ajijic"

ruta, tiempo_total = dijkstra(RED_VIAL, ORIGEN, DESTINO)

print(f"\n{'='*60}")
print("  RESULTADO FINAL")
print(f"{'='*60}")
if ruta:
    print(f"  Ruta óptima : {' → '.join(ruta)}")
    print(f"  Tiempo total: {tiempo_total} minutos")
    print(f"  Paradas     : {len(ruta) - 1} tramos")
else:
    print("  No existe ruta entre los nodos indicados.")

visualizar(RED_VIAL, ruta, ORIGEN, DESTINO, tiempo_total)