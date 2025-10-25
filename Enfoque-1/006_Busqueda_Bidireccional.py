
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
        self.acciones = acciones
        self.estados = estados
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
    return raiz
def crea_nodo_hijo(problema, padre, accion):
    nuevo_estado = problema.resultado(padre.estado, accion)
    if nuevo_estado is None: return None
    acciones_nuevo = {}
    if nuevo_estado.nombre in problema.acciones.keys():
        acciones_nuevo = problema.acciones[nuevo_estado.nombre]
    hijo = Nodo(nuevo_estado, accion, acciones_nuevo, padre)
    padre.hijos.append(hijo)
    return hijo


def invertir_acciones(acciones_originales):
    acciones_inv = {}
    for origen, dict_acciones in acciones_originales.items():
        for nombre_accion, destino in dict_acciones.items():
            if destino not in acciones_inv:
                acciones_inv[destino] = {}
            acciones_inv[destino][nombre_accion] = origen
    return acciones_inv

def nuestra_solucion_bidireccional(nodo_inicio, nodo_fin):
    camino_inicio = []
    nodo = nodo_inicio
    while nodo:
        camino_inicio.append(nodo)
        nodo = nodo.padre
    camino_inicio.reverse()

    camino_fin = []
    nodo = nodo_fin.padre
    while nodo:
        camino_fin.append(nodo)
        nodo = nodo.padre
    
    camino_fin.reverse() 
    
    print(f"Solución encontrada ({len(camino_inicio) + len(camino_fin) -1} pasos):")
    
    for nodo_camino in camino_inicio:
        print(f"Estado: {nodo_camino.estado.nombre}")
        if nodo_camino.accion:
            print(f"<--- {nodo_camino.accion.nombre} ---")

    for nodo_camino in camino_fin:
        print(f"Estado: {nodo_camino.estado.nombre}")



def busqueda_bidireccional(prob_inicio, prob_fin):
    raiz_inicio = crea_nodo_raiz(prob_inicio)
    frontera_inicio = [raiz_inicio]
    visitados_inicio = {raiz_inicio.estado: raiz_inicio}

    raiz_fin = crea_nodo_raiz(prob_fin)
    frontera_fin = [raiz_fin]
    visitados_fin = {raiz_fin.estado: raiz_fin}

    while frontera_inicio and frontera_fin:
        
        if frontera_inicio:
            nodo_actual_i = frontera_inicio.pop(0)
            
            if nodo_actual_i.estado in visitados_fin:
                print("¡Encuentro en el medio! (Detectado por búsqueda INICIO)")
                return nuestra_solucion_bidireccional(nodo_actual_i, visitados_fin[nodo_actual_i.estado])

            if not nodo_actual_i.acciones: continue # Añadido por seguridad
            for nombre_accion in nodo_actual_i.acciones.keys():
                accion = Accion(nombre_accion)
                hijo_i = crea_nodo_hijo(prob_inicio, nodo_actual_i, accion)
                
                if hijo_i and hijo_i.estado not in visitados_inicio:
                    visitados_inicio[hijo_i.estado] = hijo_i
                    frontera_inicio.append(hijo_i)

        if frontera_fin:
            nodo_actual_f = frontera_fin.pop(0)

            if nodo_actual_f.estado in visitados_inicio:
                print("¡Encuentro en el medio! (Detectado por búsqueda FIN)")
                return nuestra_solucion_bidireccional(visitados_inicio[nodo_actual_f.estado], nodo_actual_f)

            if not nodo_actual_f.acciones: continue # Añadido por seguridad
            for nombre_accion in nodo_actual_f.acciones.keys():
                accion = Accion(nombre_accion)
                hijo_f = crea_nodo_hijo(prob_fin, nodo_actual_f, accion)
                
                if hijo_f and hijo_f.estado not in visitados_fin:
                    visitados_fin[hijo_f.estado] = hijo_f
                    frontera_fin.append(hijo_f)

    print("No se ha encontrado solucion")
    return None


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

    # 4. Crear los dos problemas
    objetivo_1 = [kosos]
    problema_inicio = Problema(lanoi, objetivo_1, acciones, estados)

    estado_objetivo = objetivo_1[0]
    estado_inicial_original = lanoi
    
    acciones_inversas = invertir_acciones(acciones)
    
    problema_fin = Problema(estado_objetivo, [estado_inicial_original], acciones_inversas, estados)


    print(f"\n--- Resolviendo (lanoi -> kosos) con Búsqueda Bidireccional ---")
    busqueda_bidireccional(problema_inicio, problema_fin)