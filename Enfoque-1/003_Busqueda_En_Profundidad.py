from grafos import Accion
from grafos import Estado
from grafos import Problema
from grafos import Nodo

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

class Problema:
    def __init__(self, estado_inicial, objetivos, acciones, estados):
        self.estado_inicial = estado_inicial
        self.objetivos = objetivos
        self.acciones = acciones # El dict de acciones SIN costo
        self.estados = estados

    def es_objetivo(self, estado):
        return estado in self.objetivos

    def resultado(self, estado, accion):
        """
        Devuelve el *Estado* (objeto) resultante de tomar una acción.
        """
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
    return raiz

def crea_nodo_hijo(problema, padre, accion):
    nuevo_estado = problema.resultado(padre.estado, accion)

    if nuevo_estado is None:
        return None

    acciones_nuevo = {}
    if nuevo_estado.nombre in problema.acciones.keys():
        acciones_nuevo = problema.acciones[nuevo_estado.nombre]
    
    hijo = Nodo(nuevo_estado, accion, acciones_nuevo, padre)
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
        msg = "Estado: {0}"
        print(msg.format(nodo_camino.estado.nombre))
        if nodo_camino.accion:
            msg = "<--- {0} ---"
            print(msg.format(nodo_camino.accion.nombre))


def profundidad(problema):
    raiz = crea_nodo_raiz(problema)
    
    if problema.es_objetivo(raiz.estado):
        return raiz
        
    frontera = [raiz,] # La frontera ahora es una Pila (Stack)
    explorados = set() #no guarda valores duplicados
    
    while True:
        if not frontera:
            return None
            
        # Saca el *último* elemento (LIFO) en lugar del primero
        nodo = frontera.pop()

        explorados.add(nodo.estado)
        
        if not nodo.acciones:
            continue

        acciones_invertidas = list(nodo.acciones.keys())
        acciones_invertidas.reverse()

        for nombre_accion in acciones_invertidas:
            accion = Accion(nombre_accion)
            hijo = crea_nodo_hijo(problema, nodo, accion)

            if hijo is None:
                continue

            estados_frontera = [nodo.estado for nodo in frontera]
            
            if(hijo.estado not in explorados and hijo.estado not in estados_frontera):
                if problema.es_objetivo(hijo.estado):
                    return hijo
                frontera.append(hijo) # Se añade al final (será el próximo en salir)



if __name__ == "__main__":
    
    accN = Accion("N")
    accS = Accion("S")
    accE = Accion("E")
    accO = Accion("O")
    accNE = Accion("NE")
    accNO = Accion("NO")
    accSE = Accion("SE")
    accSO = Accion("SO")

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

    acciones = {
        'Lanoi': {'NE': 'nohoi', 'SO': 'lanoi', 'NO': 'ruun'},
        'Nohoi': {'NE': 'milos', 'SO': 'lanoi'},
        'Ruun': {'NO': 'ghiido', 'NE': 'kuart', 'E': 'milos', 'SE': 'nohoi'},
        'Milos': {'O': 'ruun', 'SO': 'nohoi', 'N': 'khandan'},
        'Ghiido': {'N': 'nokshos', 'E': 'kuart', 'SE': 'ruun'},
        'Kuart': {'O': 'ghiido', 'SO': 'ruun', 'NE': 'boomon'},
        'Boomon': {'N': 'goorum', 'SO': 'kuart'},
        'Goorum': {'O': 'shiphos', 'S': 'boomon'},
        'Shiphos': {'O': 'nokshos', 'E': 'goorum'},
        'Nokshos': {'NO': 'pharis', 'S': 'ghiido', 'E': 'shiphos'},
        'Pharis': {'NO': 'khamin', 'SO': 'nokshos'},
        'Khamin': {'SE': 'pharis', 'NO': 'tawa', 'O': 'tarios'},
        'Tarios': {'O': 'khamin', 'NO': 'tawa', 'NE': 'roria', 'E': 'peranna'},
        'Peranna': {'O': 'tarios', 'E': 'khandan'},
        'Khandan': {'O': 'peranna', 'S': 'milos'},
        'Tawa': {'SO': 'khamin', 'SE': 'tarios', 'NE': 'theer'},
        'Theer': {'SO': 'tawa', 'SE': 'roria'},
        'Roria': {'NO': 'theer', 'SO': 'tarios', 'E': 'kosos'},
        'Kosos': {'O': 'roria'}
    }

    estados = {
        'lanoi': lanoi, 'nohoi': nohoi, 'ruun': ruun, 'milos': milos,
        'ghiido': ghiido, 'kuart': kuart, 'boomon': boomon, 'goorum': goorum,
        'shiphos': shiphos, 'nokshos': nokshos, 'pharis': pharis, 'khamin': khamin,
        'tarios': tarios, 'peranna': peranna, 'khandan': khandan, 'tawa': tawa,
        'theer': theer, 'roria': roria, 'kosos': kosos
    }

    # 5. Crear y Resolver el Problema
    objetivo_1 = [kosos]
    problema_1 = Problema(lanoi, objetivo_1, acciones, estados)

    print("--- Resolviendo Problema 1 (Objetivo: Kosos) con DFS ---")
    solucion = profundidad(problema_1)
    nuestra_solucion(solucion)