from grafos import Accion
from grafos import Estado
from grafos import Problema
from grafos import Nodo


def anchura(problema):
    raiz = crea_nodo_raiz(problema)
    if problema.es_objetivo(raiz.estado):
        return raiz
    frontera = [raiz,]
    explorados = set() #no guarda valores duplicados
    while True:
        if not frontera:
            return None
        nodo = frontera.pop(0)
        explorados.add(nodo.estado)
        if not nodo.acciones:
            continue
        for nombre_accion in nodo.acciones.keys():
            accion = Accion(nombre_accion)
            hijo = crea_nodo_hijo(problema, nodo, accion)
            estados_frontera = [nodo.estado for nodo in frontera]
            if(hijo.estado not in explorados and hijo.estado not in estados_frontera):
                if problema.es_objetivo(hijo.estado):
                    return hijo
                frontera.append(hijo)


def crea_nodo_raiz(problema):
    estado_raiz = problema.estado_inicial
    acciones_raiz = {}
    if estado_raiz.nombre in problema.acciones.keys():
        acciones_raiz = problema.acciones[estado_raiz.nombre]
    raiz = Nodo(estado_raiz, None, acciones_raiz, None)
    return raiz

def crea_nodo_hijo(problema, padre, accion):
    nuevo_estado = problema.resultado(padre.estado, accion)
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
    nodo = objetivo 
    while nodo:
        msg = "Estado: {0}"
        print(msg.format(nodo.estado.nombre))
        if nodo.accion:
            msg = "<--- {0} ---"
            print(msg.format(nodo.accion.nombre))
        nodo = nodo.padre


if __name__ == "__main__":
    accN = Accion("N")
    accS = Accion("S")
    accE = Accion("E")
    accO = Accion("O")
    accNE = Accion("NE")
    accNO = Accion("NO")
    accSE = Accion("SE")
    accSO = Accion("SO")

    lanoi = Estado("Lanoi", [accNE])
    nohoi = Estado("Nohoi", [accSO, accNO, accNE])
    ruun = Estado("Ruun", [accNO, accNE, accE, accSE])
    milos = Estado("Milos", [accO, accSO, accN])
    ghiido = Estado("Ghiido", [accN, accE, accSE])
    kuart = Estado("Kuart", [accO, accSO, accNE])
    boomon = Estado("Boomon", [accN, accSO])
    goorum = Estado("Goorum", [accO, accS])
    shiphos = Estado("Shiphos", [accO, accE])
    nokshos = Estado("Nokshos", [accNO, accS, accE])
    pharis = Estado("Pharis", [accNO, accSO])
    khamin = Estado("Khamin", [accSE, accNO, accO])
    tarios = Estado("Tarios", [accO, accNO, accNE, accE])
    peranna = Estado("Peranna", [accO, accE])
    khandan = Estado("Khandan", [accO, accS])
    tawa = Estado("Tawa", [accSO, accSE, accNE])
    theer = Estado("Theer", [accSO, accSE])
    roria = Estado("Roria", [accNO, accSO, accE])
    kosos = Estado("Kosos", [accO])

    acciones = {
    'Lanoi': {'NE': 'nohoi',
              'SO': 'lanoi',
              'NO': 'ruun'},
    'Nohoi': {'NE': 'milos'},
    'Ruun': {'NO': 'ghiido',
             'NE': 'kuart',
             'E': 'milos',
             'SE': 'nohoi'},
    'Milos': {'O': 'ruun',
              'SO': 'nohoi',
              'N': 'khandan'},
    'Ghiido': {'N': 'nokshos',
               'E': 'kuart',
               'SE': 'ruun'},
    'Kuart': {'O': 'ghiido',
              'SO': 'ruun',
              'NE': 'boomon'},
    'Boomon': {'N': 'goorum',
               'SO': 'kuart'},
    'Goorum': {'O': 'shiphos',
               'S': 'boomon'},
    'Shiphos': {'O': 'nokshos',
                'E': 'goorum'},
    'Nokshos': {'NO': 'pharis',
                'S': 'ghiido',
                'E': 'shiphos'},
    'Pharis': {'NO': 'khamin',
               'SO': 'nokshos'},
    'Khamin': {'SE': 'pharis',
               'NO': 'tawa',
               'O': 'tarios'},
    'Tarios': {'O': 'khamin',
               'NO': 'tawa',
               'NE': 'roria',
               'E': 'peranna'},
    'Peranna': {'O': 'tarios',
                'E': 'khandan'},
    'Khandan': {'O': 'peranna',
                'S': 'milos'},
    'Tawa': {'SO': 'khamin',
             'SE': 'tarios',
             'NE': 'theer'},
    'Theer': {'SO': 'tawa',
              'SE': 'roria'},
    'Roria': {'NO': 'theer',
              'SO': 'tarios',
              'E': 'kosos'},
    'Kosos': {'O': 'roria'}}

    # Diccionario de estados para que el problema pueda convertir nombres a objetos Estado
    estados = {
        'lanoi': lanoi,
        'nohoi': nohoi,
        'ruun': ruun,
        'milos': milos,
        'ghiido': ghiido,
        'kuart': kuart,
        'boomon': boomon,
        'goorum': goorum,
        'shiphos': shiphos,
        'nokshos': nokshos,
        'pharis': pharis,
        'khamin': khamin,
        'tarios': tarios,
        'peranna': peranna,
        'khandan': khandan,
        'tawa': tawa,
        'theer': theer,
        'roria': roria,
        'kosos': kosos
    }

objetivo_1 = [kosos]
problema_1 = Problema(lanoi, objetivo_1, acciones, estados)

objetivo_2 = [goorum]
problema_2 = Problema(lanoi, objetivo_2, acciones, estados)

objetivo_3 = [boomon, goorum]
problema_3 = Problema(lanoi, objetivo_3, acciones, estados)

problema_resolver = problema_1


solucion = anchura(problema_resolver)
nuestra_solucion(solucion)