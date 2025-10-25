from grafos import Accion
from grafos import Estado
from grafos import Problema
from grafos import Nodo



class Estado:
    """
    Representa un estado en el espacio de búsqueda.
    """
    def __init__(self, nombre, acciones=None):
        self.nombre = nombre
    
    def __eq__(self, other):
        return isinstance(other, Estado) and self.nombre == other.nombre
    
    def __hash__(self):
        return hash(self.nombre)

class Accion:
    """
    Representa una acción que se puede tomar.
    """
    def __init__(self, nombre):
        self.nombre = nombre

class Nodo:
    """
    Representa un nodo en el árbol de búsqueda.
    """
    def __init__(self, estado, accion, acciones, padre):
        self.estado = estado
        self.accion = accion # Acción que llevó a este estado
        self.acciones = acciones # Acciones posibles *desde* este estado
        self.padre = padre
        self.hijos = []
        
        self.costo_camino = 0 

    def __lt__(self, other):
        return self.costo_camino < other.costo_camino

class Problema:
    """
    Define el problema: estado inicial, objetivos, y el modelo de transición.
    """
    def __init__(self, estado_inicial, objetivos, acciones, estados):
        self.estado_inicial = estado_inicial
        self.objetivos = objetivos # Lista de estados objetivo
        self.acciones = acciones # Dict de acciones CON COSTO
        self.estados = estados # Dict de nombre_str -> Objeto Estado

    def es_objetivo(self, estado):
        """Comprueba si un estado es uno de los objetivos."""
        return estado in self.objetivos

    def obtener_costo_accion(self, estado_origen, accion):
        """
        Obtiene el costo de una acción desde un estado.
        """
        if estado_origen.nombre in self.acciones:
            if accion.nombre in self.acciones[estado_origen.nombre]:
                return self.acciones[estado_origen.nombre][accion.nombre][1]
        return 0 # Costo cero si la acción no existe (o infinito)

    def resultado(self, estado, accion):
        """
        Devuelve el *Estado* (objeto) resultante de tomar una acción.
        """
        if estado.nombre in self.acciones:
            if accion.nombre in self.acciones[estado.nombre]:
                nombre_estado_hijo = self.acciones[estado.nombre][accion.nombre][0]
                return self.estados[nombre_estado_hijo]
        return None


def crea_nodo_raiz(problema):
    estado_raiz = problema.estado_inicial
    acciones_raiz = {}
    if estado_raiz.nombre in problema.acciones.keys():
        acciones_raiz = problema.acciones[estado_raiz.nombre]
    raiz = Nodo(estado_raiz, None, acciones_raiz, None)
    raiz.costo_camino = 0 # El costo para llegar a la raíz es 0
    return raiz

def crea_nodo_hijo(problema, padre, accion):
    nuevo_estado = problema.resultado(padre.estado, accion)
    
    if nuevo_estado is None:
        return None

    acciones_nuevo = {}
    if nuevo_estado.nombre in problema.acciones.keys():
        acciones_nuevo = problema.acciones[nuevo_estado.nombre]
    
    hijo = Nodo(nuevo_estado, accion, acciones_nuevo, padre)
    
    costo_accion = problema.obtener_costo_accion(padre.estado, accion)
    hijo.costo_camino = padre.costo_camino + costo_accion
    
    padre.hijos.append(hijo)
    return hijo

def nuestra_solucion(objetivo=None):
    """
    Imprime la solución desde el nodo objetivo de vuelta a la raíz.
    """
    if not objetivo:
        print("No se ha encontrado solucion")
        return
    
    print(f"Solución encontrada con costo total: {objetivo.costo_camino}")
    nodos_camino = []
    nodo = objetivo 
    while nodo:
        nodos_camino.append(nodo)
        nodo = nodo.padre
    
    nodos_camino.reverse()
    for i, nodo_camino in enumerate(nodos_camino):
        msg = "Estado: {0}"
        print(msg.format(nodo_camino.estado.nombre))
        if nodo_camino.accion:
            msg = "<--- {0} (Costo: {1}) ---"
            costo_paso = nodo_camino.costo_camino - (nodo_camino.padre.costo_camino if nodo_camino.padre else 0)
            print(msg.format(nodo_camino.accion.nombre, costo_paso))



def costo_uniforme(problema):
    raiz = crea_nodo_raiz(problema)
    
    frontera = [raiz,]
    explorados = set()
    
    while True:
        if not frontera:
            return None 

        frontera.sort(key=lambda nodo: nodo.costo_camino) 

        nodo = frontera.pop(0)
        

        if problema.es_objetivo(nodo.estado):
            return nodo
        
        explorados.add(nodo.estado)
        
        if not nodo.acciones:
            continue
            
        for nombre_accion in nodo.acciones.keys():
            accion = Accion(nombre_accion)
            hijo = crea_nodo_hijo(problema, nodo, accion)

            if hijo is None:
                continue

            nodo_en_frontera = None
            for n_frontera in frontera:
                if n_frontera.estado == hijo.estado:
                    nodo_en_frontera = n_frontera
                    break
            
            if hijo.estado not in explorados and not nodo_en_frontera:
                frontera.append(hijo)

            elif nodo_en_frontera and hijo.costo_camino < nodo_en_frontera.costo_camino:
                frontera.remove(nodo_en_frontera) 
                frontera.append(hijo)


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

    # 4. Diccionario de consulta de Estados
    estados = {
        'lanoi': lanoi, 'nohoi': nohoi, 'ruun': ruun, 'milos': milos,
        'ghiido': ghiido, 'kuart': kuart, 'boomon': boomon, 'goorum': goorum,
        'shiphos': shiphos, 'nokshos': nokshos, 'pharis': pharis, 'khamin': khamin,
        'tarios': tarios, 'peranna': peranna, 'khandan': khandan, 'tawa': tawa,
        'theer': theer, 'roria': roria, 'kosos': kosos
    }

    
    # Problema 1: Encontrar el camino más barato a Kosos
    objetivo_1 = [kosos]
    problema_1 = Problema(lanoi, objetivo_1, acciones_con_costo, estados)

    # Problema 2: Encontrar el camino más barato a Goorum
    objetivo_2 = [goorum]
    problema_2 = Problema(lanoi, objetivo_2, acciones_con_costo, estados)


    print("--- Resolviendo Problema 1 (Objetivo: Kosos) ---")
    solucion_1 = costo_uniforme(problema_1)
    nuestra_solucion(solucion_1)

    print("\n--- Resolviendo Problema 2 (Objetivo: Goorum) ---")
    solucion_2 = costo_uniforme(problema_2)
    nuestra_solucion(solucion_2)