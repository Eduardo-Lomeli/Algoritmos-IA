from grafos import Accion
from grafos import Estado
from grafos import Problema
from grafos import Nodo


def anchura(problema):
    raiz = crea_nodo_raiz(problema)

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

    acciones acciones = {
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

objetivo_1 = [kosos]
problema_1 = Problema(lanoi, objetivo_1, acciones)

objetivo_2 = [goorum]
problema_2 = Problema(lanoi, objetivo_2, acciones)

objetivo_3 = [boomon, goorum]
problema_3 = Problema(lanoi, objetivo_3, acciones)

problema_resolver = problema_1
