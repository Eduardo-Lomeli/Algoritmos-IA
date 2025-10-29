import random
from collections import deque


class Estado:
    def __init__(self, nombre):
        self.nombre = nombre
    def __eq__(self, other):
        return isinstance(other, Estado) and self.nombre == other.nombre
    def __hash__(self):
        return hash(self.nombre)
    def __repr__(self):
        return f"Estado({self.nombre})"

class Problema:
    def __init__(self, acciones, estados, heuristica_h):
        # Nota: no hay estado inicial ni objetivo
        self.acciones = acciones 
        self.estados = estados # dict de nombre -> objeto Estado
        self.heuristica_h = heuristica_h

    def obtener_vecinos(self, estado_actual):
        """
        Devuelve una lista de objetos Estado que son vecinos del estado actual.
        """
        vecinos = []
        if estado_actual.nombre in self.acciones:
            nombres_vecinos = self.acciones[estado_actual.nombre].values()
            for nombre in nombres_vecinos:
                if nombre in self.estados:
                    vecinos.append(self.estados[nombre])
        return vecinos

    def evaluar(self, estado):
        """
        Función de evaluación. Queremos minimizar esto.
        Devuelve el valor h(n) del estado.
        """
        return self.heuristica_h.get(estado.nombre, float('inf'))

def busqueda_tabu(problema, max_iteraciones, tenencia_tabu):
    """
    Realiza la Búsqueda Tabú.
    - tenencia_tabu: Cuántas iteraciones un estado permanece en la lista tabú.
    """
    
    # 1. Iniciar en un estado aleatorio
    estado_aleatorio = random.choice(list(problema.estados.values()))
    solucion_actual = estado_aleatorio
    mejor_solucion_global = solucion_actual
    
    lista_tabu = deque(maxlen=tenencia_tabu)
    
    print(f"Iniciando en: {solucion_actual.nombre} (h={problema.evaluar(solucion_actual)})")
    
    for i in range(max_iteraciones):
        # 2. Obtener todos los vecinos del estado actual
        vecinos = problema.obtener_vecinos(solucion_actual)
        
        if not vecinos:
            continue # Atascado en un nodo sin salida

        mejor_vecino_encontrado = None
        mejor_evaluacion_vecino = float('inf')

        for vecino in vecinos:
            evaluacion_vecino = problema.evaluar(vecino)
            
            es_tabu = vecino in lista_tabu
            

            if evaluacion_vecino < problema.evaluar(mejor_solucion_global):
                es_tabu = False # Aspiración: permitir si es mejor que la mejor solución global
                
            # 4. Seleccionar el mejor vecino que NO sea tabú
            if not es_tabu and evaluacion_vecino < mejor_evaluacion_vecino:
                mejor_vecino_encontrado = vecino
                mejor_evaluacion_vecino = evaluacion_vecino

        if mejor_vecino_encontrado is None:
            continue

        solucion_actual = mejor_vecino_encontrado

        lista_tabu.append(solucion_actual)
        
        # 7. Actualizar la mejor solución global si es necesario
        if problema.evaluar(solucion_actual) < problema.evaluar(mejor_solucion_global):
            mejor_solucion_global = solucion_actual
            print(f"  Iter {i}: ¡Nueva mejor solución global! {mejor_solucion_global.nombre} (h={problema.evaluar(mejor_solucion_global)})")
        
        print(f"  Iter {i}: Moviendo a {solucion_actual.nombre} (h={problema.evaluar(solucion_actual)})")

    return mejor_solucion_global


if __name__ == "__main__":
    
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
        'ghiido': 7, 'kuart': 7, 'boomon': 6, # Óptimo local
        'goorum': 7, 'shiphos': 6, 'nokshos': 6, 'pharis': 5, 'khamin': 4,
        'tarios': 2, 'peranna': 3, 'khandan': 4, 'tawa': 3,
        'theer': 2, 'roria': 1, 'kosos': 0 # Óptimo global
    }

    # 5. Crear y Resolver el Problema
    problema_optimizacion = Problema(acciones, estados, heuristica_h_a_kosos)

    # Parámetros de Búsqueda Tabú
    MAX_ITERACIONES = 50
    TENENCIA_TABU = 5 # Los estados permanecen 5 iteraciones en la lista

    print(f"\n--- Resolviendo (Encontrar mejor estado) con Búsqueda Tabú ---")
    solucion = busqueda_tabu(problema_optimizacion, MAX_ITERACIONES, TENENCIA_TABU)
    
    print("\n--- Búsqueda finalizada ---")
    print(f"La mejor solución global encontrada fue: {solucion.nombre}")
    print(f"Valor de evaluación (h(n)): {problema_optimizacion.evaluar(solucion)}")