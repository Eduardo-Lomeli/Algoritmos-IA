
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
        self.costo_camino = 0
        
        # Valor de la heurística h(n)
        self.heuristica = 0

class Problema:
    def __init__(self, estado_inicial, objetivos, acciones, estados, heuristica_h):
        self.estado_inicial = estado_inicial
        self.objetivos = objetivos
        self.acciones = acciones # Dict de acciones (con o sin costo)
        self.estados = estados
        
        # Dict de valores heurísticos
        self.heuristica_h = heuristica_h

    def es_objetivo(self, estado):
        return estado in self.objetivos

    def resultado(self, estado, accion):
        # Esta función puede usar el dict de acciones con o sin costo
        if estado.nombre in self.acciones:
            if accion.nombre in self.acciones[estado.nombre]:
                destino = self.acciones[estado.nombre][accion.nombre]
                # Maneja ambos formatos: ('estado', costo) o 'estado'
                if isinstance(destino, tuple):
                    nombre_estado_hijo = destino[0]
                else:
                    nombre_estado_hijo = destino
                return self.estados[nombre_estado_hijo]
        return None
    

def crea_nodo_raiz(problema):
    estado_raiz = problema.estado_inicial
    acciones_raiz = {}
    if estado_raiz.nombre in problema.acciones.keys():
        acciones_raiz = problema.acciones[estado_raiz.nombre]
    raiz = Nodo(estado_raiz, None, acciones_raiz, None)
    
    raiz.costo_camino = 0
    raiz.heuristica = problema.heuristica_h.get(raiz.estado.nombre, 0)
    
    return raiz

def crea_nodo_hijo(problema, padre, accion):
    nuevo_estado = problema.resultado(padre.estado, accion)
    if nuevo_estado is None: return None

    acciones_nuevo = {}
    if nuevo_estado.nombre in problema.acciones.keys():
        acciones_nuevo = problema.acciones[nuevo_estado.nombre]
    
    hijo = Nodo(nuevo_estado, accion, acciones_nuevo, padre)
    
    hijo.heuristica = problema.heuristica_h.get(hijo.estado.nombre, 0)
    
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
    
    print(f"Solución encontrada ({len(nodos_camino) - 1} pasos):")
    
    for i, nodo_camino in enumerate(nodos_camino):
        msg = "Estado: {0} (h(n)={1})"
        print(msg.format(nodo_camino.estado.nombre, nodo_camino.heuristica))
        if nodo_camino.accion:
            msg = "<--- {0} ---"
            print(msg.format(nodo_camino.accion.nombre))


def busqueda_voraz(problema):
    raiz = crea_nodo_raiz(problema)
    
    # La cola de prioridad
    frontera = [raiz,]
    
    # Conjunto de estados ya explorados
    explorados = set()
    
    while True:
        if not frontera:
            return None # No se encontró solución
        
        frontera.sort(key=lambda nodo: nodo.heuristica)
        
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

            if hijo.estado not in explorados:
                # Comprobar si ya está en la frontera
                estados_frontera = [n.estado for n in frontera]
                if hijo.estado not in estados_frontera:
                     frontera.append(hijo)



if __name__ == "__main__":
    
    accN = Accion("N"); accS = Accion("S"); accE = Accion("E"); accO = Accion("O")
    accNE = Accion("NE"); accNO = Accion("NO"); accSE = Accion("SE"); accSO = Accion("SO")
    
    lanoi = Estado("lanoi"); nohoi = Estado("nohoi"); ruun = Estado("ruun")
    milos = Estado("milos"); ghiido = Estado("ghiido"); kuart = Estado("kuart")
    boomon = Estado("boomon"); goorum = Estado("goorum"); shiphos = Estado("shiphos")
    nokshos = Estado("nokshos"); pharis = Estado("pharis"); khamin = Estado("khamin")
    tarios = Estado("tarios"); peranna = Estado("peranna"); khandan = Estado("khandan")
    tawa = Estado("tawa"); theer = Estado("theer"); roria = Estado("roria"); kosos = Estado("kosos")

    acciones = {
        'lanoi': {'NE': 'nohoi', 'SO': 'lanoi', 'NO': 'ruun'},
        'nohoi': {'NE': 'milos', 'SO': 'lanoi'},
        'ruun': {'NO': 'ghiido', 'NE': 'kuart', 'E': 'milos', 'SE': 'nohoi'},
        'milos': {'O': 'ruun', 'SO': 'nohoi', 'N': 'khandan'},
        'ghiido': {'N': 'nokshos', 'E': 'kuart', 'SE': 'ruun'},
        'kuart': {'O': 'ghiido', 'SO': 'ruun', 'NE': 'boomon'},
        'boomon': {'N': 'goorum', 'SO': 'kuart'},
        'goorum': {'O': 'shiphos', 'S': 'boomon'},
        'shiphos': {'O': 'nokshos', 'E': 'goorum'},
        'nokshos': {'NO': 'pharis', 'S': 'ghiido', 'E': 'shiphos'},
        'pharis': {'NO': 'khamin', 'SO': 'nokshos'},
        'khamin': {'SE': 'pharis', 'NO': 'tawa', 'O': 'tarios'},
        'tarios': {'O': 'khamin', 'NO': 'tawa', 'NE': 'roria', 'E': 'peranna'},
        'peranna': {'O': 'tarios', 'E': 'khandan'},
        'khandan': {'O': 'peranna', 'S': 'milos'},
        'tawa': {'SO': 'khamin', 'SE': 'tarios', 'NE': 'theer'},
        'theer': {'SO': 'tawa', 'SE': 'roria'},
        'roria': {'NO': 'theer', 'SO': 'tarios', 'E': 'kosos'},
        'kosos': {'O': 'roria'}
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
    problema_1 = Problema(lanoi, objetivo_1, acciones, estados, heuristica_h_a_kosos)

    print(f"\n--- Resolviendo (lanoi -> kosos) con Búsqueda Voraz ---")
    solucion = busqueda_voraz(problema_1)
    nuestra_solucion(solucion)