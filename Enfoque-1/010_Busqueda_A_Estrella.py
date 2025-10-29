
class Estado:
    def __init__(self, nombre, acciones=None):
        self.nombre = nombre
    def __eq__(self, other):
        return isinstance(other, Estado) and self.nombre == other.nombre
    def __hash__(self):
        return hash(self.nombre)
class Accion:
    def __init__(self, nombre):
        self.nombre = nombre

class Nodo:
    def __init__(self, estado, accion, acciones, padre):
        self.estado = estado
        self.accion = accion
        self.acciones = acciones
        self.padre = padre
        self.hijos = []
        
        # g(n): Costo real del camino desde el inicio
        self.costo_camino = 0
        # h(n): Costo estimado al objetivo
        self.heuristica = 0
        # f(n) = g(n) + h(n): Costo total estimado
        self.costo_f = 0

    def __lt__(self, other):
        return self.costo_f < other.costo_f

class Problema:
    def __init__(self, estado_inicial, objetivos, acciones, estados, heuristica_h):
        self.estado_inicial = estado_inicial
        self.objetivos = objetivos
        self.acciones = acciones 
        self.estados = estados
        self.heuristica_h = heuristica_h

    def es_objetivo(self, estado):
        return estado in self.objetivos

    def obtener_costo_accion(self, estado_origen, accion):
        if estado_origen.nombre in self.acciones:
            if accion.nombre in self.acciones[estado_origen.nombre]:
                # acciones = {'lanoi': {'NE': ('nohoi', 3)}}
                return self.acciones[estado_origen.nombre][accion.nombre][1]
        return 0

    def resultado(self, estado, accion):
        if estado.nombre in self.acciones:
            if accion.nombre in self.acciones[estado.nombre]:
                # acciones = {'lanoi': {'NE': ('nohoi', 3)}}
                nombre_estado_hijo = self.acciones[estado.nombre][accion.nombre][0]
                return self.estados[nombre_estado_hijo]
        return None

def crea_nodo_raiz(problema):
    estado_raiz = problema.estado_inicial
    acciones_raiz = {}
    if estado_raiz.nombre in problema.acciones.keys():
        acciones_raiz = problema.acciones[estado_raiz.nombre]
    raiz = Nodo(estado_raiz, None, acciones_raiz, None)
    
    raiz.costo_camino = 0 # g(n) = 0
    raiz.heuristica = problema.heuristica_h.get(raiz.estado.nombre, 0) # h(n)
    raiz.costo_f = raiz.costo_camino + raiz.heuristica # f(n) = g(n) + h(n)
    
    return raiz

def crea_nodo_hijo(problema, padre, accion):
    nuevo_estado = problema.resultado(padre.estado, accion)
    if nuevo_estado is None: return None

    acciones_nuevo = {}
    if nuevo_estado.nombre in problema.acciones.keys():
        acciones_nuevo = problema.acciones[nuevo_estado.nombre]
    
    hijo = Nodo(nuevo_estado, accion, acciones_nuevo, padre)
    
    # Calcular g(n), h(n) y f(n)
    costo_accion = problema.obtener_costo_accion(padre.estado, accion)
    hijo.costo_camino = padre.costo_camino + costo_accion # g(n)
    hijo.heuristica = problema.heuristica_h.get(hijo.estado.nombre, 0) # h(n)
    hijo.costo_f = hijo.costo_camino + hijo.heuristica # f(n)
    
    padre.hijos.append(hijo)
    return hijo

def nuestra_solucion(objetivo=None):
    if not objetivo:
        print("No se ha encontrado solucion")
        return
    
    nodos_camino = []
    nodo = objetivo 
    while nodo:
        nodos_camino.append(nodo)
        nodo = nodo.padre
    nodos_camino.reverse()
    
    print(f"Solución ÓPTIMA encontrada (Costo g(n): {objetivo.costo_camino}, f(n)={objetivo.costo_f}):")
    
    for i, nodo_camino in enumerate(nodos_camino):
        # Imprimimos todo para ver la lógica de A*
        msg = "Estado: {0} (g(n)={1}, h(n)={2}, f(n)={3})"
        print(msg.format(nodo_camino.estado.nombre, 
                         nodo_camino.costo_camino, 
                         nodo_camino.heuristica, 
                         nodo_camino.costo_f))
        if nodo_camino.accion:
            costo_paso = nodo_camino.costo_camino - nodo_camino.padre.costo_camino
            print(f"<--- {nodo_camino.accion.nombre} (Costo: {costo_paso}) ---")


# --- Algoritmo de Búsqueda A* ---

def busqueda_a_estrella(problema):
    raiz = crea_nodo_raiz(problema)
    
    frontera = [raiz,] # Cola de Prioridad
    explorados = set() # Estados ya expandidos
    
    while True:
        if not frontera:
            return None # No se encontró solución
        
        frontera.sort(key=lambda nodo: nodo.costo_f)

        nodo = frontera.pop(0)
        if problema.es_objetivo(nodo.estado):
            return nodo
        
        explorados.add(nodo.estado)
        
        if not nodo.acciones:
            continue
            
        for nombre_accion in nodo.acciones.keys():
            accion = Accion(nombre_accion)
            hijo = crea_nodo_hijo(problema, nodo, accion)

            if hijo is None: continue

            # Comprobar si ya lo hemos expandido
            if hijo.estado in explorados:
                continue

            # Comprobar si está en la frontera
            nodo_en_frontera = None
            for n_frontera in frontera:
                if n_frontera.estado == hijo.estado:
                    nodo_en_frontera = n_frontera
                    break
            
            if not nodo_en_frontera:
                frontera.append(hijo)
            elif hijo.costo_camino < nodo_en_frontera.costo_camino:
                frontera.remove(nodo_en_frontera) # Quitar el caro
                frontera.append(hijo) # Poner el barato


if __name__ == "__main__":
    

    accN = Accion("N"); accS = Accion("S"); accE = Accion("E"); accO = Accion("O")
    accNE = Accion("NE"); accNO = Accion("NO"); accSE = Accion("SE"); accSO = Accion("SO")
    
    lanoi = Estado("lanoi"); nohoi = Estado("nohoi"); ruun = Estado("ruun")
    milos = Estado("milos"); ghiido = Estado("ghiido"); kuart = Estado("kuart")
    boomon = Estado("boomon"); goorum = Estado("goorum"); shiphos = Estado("shiphos")
    nokshos = Estado("nokshos"); pharis = Estado("pharis"); khamin = Estado("khamin")
    tarios = Estado("tarios"); peranna = Estado("peranna"); khandan = Estado("khandan")
    tawa = Estado("tawa"); theer = Estado("theer"); roria = Estado("roria"); kosos = Estado("kosos")
    # Usamos las acciones CON COSTO
    acciones_con_costo = {
        'lanoi': {'NE': ('nohoi', 3), 'SO': ('lanoi', 1), 'NO': ('ruun', 5)},
        'nohoi': {'NE': ('milos', 4), 'SO': ('lanoi', 3)},
        'ruun': {'NO': ('ghiido', 6), 'NE': ('kuart', 5), 'E': ('milos', 3), 'SE': ('nohoi', 2)},
        'milos': {'O': ('ruun', 3), 'SO': ('nohoi', 4), 'N': ('khandan', 10)},
        'ghiido': {'N': ('nokshos', 7), 'E': ('kuart', 2), 'SE': ('ruun', 6)},
        'kuart': {'O': ('ghiido', 2), 'SO': ('ruun', 5), 'NE': ('boomon', 3)},
        'boomon': {'N': ('goorum', 2), 'SO': ('kuart', 3)},
        'goorum': {'O': ('shiphos', 4), 'S': ('boomon', 2)},
        'shiphos': {'O': ('nokshos', 5), 'E': ('goorum', 4)},
        'nokshos': {'NO': ('pharis', 3), 'S': ('ghiido', 7), 'E': ('shiphos', 5)},
        'pharis': {'NO': ('khamin', 4), 'SO': ('nokshos', 3)},
        'khamin': {'SE': ('pharis', 4), 'NO': ('tawa', 6), 'O': ('tarios', 5)},
        'tarios': {'O': ('khamin', 5), 'NO': ('tawa', 3), 'NE': ('roria', 4), 'E': ('peranna', 2)},
        'peranna': {'O': ('tarios', 2), 'E': ('khandan', 3)},
        'khandan': {'O': ('peranna', 3), 'S': ('milos', 10)},
        'tawa': {'SO': ('khamin', 6), 'SE': ('tarios', 3), 'NE': ('theer', 2)},
        'theer': {'SO': ('tawa', 2), 'SE': ('roria', 3)},
        'roria': {'NO': ('theer', 3), 'SO': ('tarios', 4), 'E': ('kosos', 5)},
        'kosos': {'O': ('roria', 5)}
    }
    
    estados = {
        'lanoi': lanoi, 'nohoi': nohoi, 'ruun': ruun, 'milos': milos,
        'ghiido': ghiido, 'kuart': kuart, 'boomon': boomon, 'goorum': goorum,
        'shiphos': shiphos, 'nokshos': nokshos, 'pharis': pharis, 'khamin': khamin,
        'tarios': tarios, 'peranna': peranna, 'khandan': khandan, 'tawa': tawa,
        'theer': theer, 'roria': roria, 'kosos': kosos
    }
    
    heuristica_h_a_kosos = {
        'lanoi': 10, 'nohoi': 9, 'ruun': 8, 'milos': 8,
        'ghiido': 7, 'kuart': 7, 'boomon': 6, 'goorum': 7,
        'shiphos': 6, 'nokshos': 6, 'pharis': 5, 'khamin': 4,
        'tarios': 2, 'peranna': 3, 'khandan': 4, 'tawa': 3,
        'theer': 2, 'roria': 1, 'kosos': 0
    }

    # 5. Crear y Resolver el Problema
    objetivo_1 = [kosos]
    problema_1 = Problema(lanoi, objetivo_1, acciones_con_costo, estados, heuristica_h_a_kosos)

    print(f"\n--- Resolviendo (lanoi -> kosos) con Búsqueda A* ---")
    solucion = busqueda_a_estrella(problema_1)
    nuestra_solucion(solucion)