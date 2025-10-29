
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
        self.padre = padre # No lo usaremos, pero lo mantenemos por consistencia
        self.hijos = []
        self.heuristica = 0 # h(n)

class Problema:
    def __init__(self, estado_inicial, objetivos, acciones, estados, heuristica_h):
        self.estado_inicial = estado_inicial
        self.objetivos = objetivos
        self.acciones = acciones
        self.estados = estados
        self.heuristica_h = heuristica_h

    def es_objetivo(self, estado):
        return estado in self.objetivos

    def resultado(self, estado, accion):
        if estado.nombre in self.acciones:
            if accion.nombre in self.acciones[estado.nombre]:
                nombre_estado_hijo = self.acciones[estado.nombre][accion.nombre]
                return self.estados[nombre_estado_hijo]
        return None

def crea_nodo_raiz(problema):
    estado_raiz = problema.estado_inicial
    acciones_raiz = {}
    if estado_raiz.nombre in problema.acciones.keys():
        acciones_raiz = problema.acciones[estado_raiz.nombre]
    raiz = Nodo(estado_raiz, None, acciones_raiz, None)
    raiz.heuristica = problema.heuristica_h.get(raiz.estado.nombre, 0)
    return raiz

def crea_nodo_hijo(problema, padre, accion):
    nuevo_estado = problema.resultado(padre.estado, accion)
    if nuevo_estado is None: return None
    acciones_nuevo = {}
    if nuevo_estado.nombre in problema.acciones.keys():
        acciones_nuevo = problema.acciones[nuevo_estado.nombre]
    
    hijo = Nodo(nuevo_estado, accion, acciones_nuevo, padre)
    hijo.heuristica = problema.heuristica_h.get(hijo.estado.nombre, 0) # h(n)
    
    padre.hijos.append(hijo)
    return hijo


def ascension_colinas(problema):
    """
    Búsqueda de Ascensión de Colinas.
    Intenta minimizar el valor de la heurística.
    """
    nodo_actual = crea_nodo_raiz(problema)
    print(f"Comenzando en: {nodo_actual.estado.nombre} (h(n)={nodo_actual.heuristica})")
    
    while True:
        mejor_vecino = None
        mejor_heuristica = nodo_actual.heuristica 
        
        if not nodo_actual.acciones:
            break 
            
        for nombre_accion in nodo_actual.acciones.keys():
            accion = Accion(nombre_accion)
            vecino = crea_nodo_hijo(problema, nodo_actual, accion)
            if vecino is None: continue
            
            # 2. Encontrar el *mejor* vecino
            if vecino.heuristica < mejor_heuristica:
                mejor_vecino = vecino
                mejor_heuristica = vecino.heuristica
        
        # 3. Decidir si moverse o detenerse
        if mejor_vecino is None:
            print("No se encontraron vecinos mejores. Mínimo local alcanzado.")
            return nodo_actual
        
        # Moverse al mejor vecino encontrado
        nodo_actual = mejor_vecino
        print(f"Moviendo a -> {nodo_actual.estado.nombre} (h(n)={nodo_actual.heuristica})")


def mostrar_resultado_local(nodo_final):
    """
    Imprime el resultado de una búsqueda local (sólo el estado final).
    """
    if not nodo_final:
        print("No se encontró solución.")
        return
    print("\n--- Resultado Final (Pico/Mínimo Local) ---")
    print(f"Estado: {nodo_final.estado.nombre}")
    print(f"Valor Heurístico: {nodo_final.heuristica}")


if __name__ == "__main__":

    accN = Accion("N"); accS = Accion("S"); accE = Accion("E"); accO = Accion("O")
    accNE = Accion("NE"); accNO = Accion("NO"); accSE = Accion("SE"); accSO = Accion("SO")
    
    lanoi = Estado("lanoi"); nohoi = Estado("nohoi"); ruun = Estado("ruun")
    milos = Estado("milos"); ghiido = Estado("ghiido"); kuart = Estado("kuart")
    boomon = Estado("boomon"); goorum = Estado("goorum"); shiphos = Estado("shiphos")
    nokshos = Estado("nokshos"); pharis = Estado("pharis"); khamin = Estado("khamin")
    tarios = Estado("tarios"); peranna = Estado("peranna"); khandan = Estado("khandan")
    tawa = Estado("tawa"); theer = Estado("theer"); roria = Estado("roria"); kosos = Estado("kosos")

    # Usamos las acciones sin costo
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
    
    # Usamos la misma Heurística
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

    print(f"\n--- Resolviendo (lanoi -> ???) con Ascensión de Colinas ---")
    solucion_local = ascension_colinas(problema_1)
    mostrar_resultado_local(solucion_local)