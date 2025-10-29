import random


class Estado:
    def __init__(self, nombre):
        self.nombre = nombre
    def __eq__(self, other):
        return isinstance(other, Estado) and self.nombre == other.nombre
    def __hash__(self):
        return hash(self.nombre)
    def __repr__(self):
        # Ayuda a depurar
        return f"Estado({self.nombre}, h={_problema_global_temp.evaluar(self) if _problema_global_temp else 'N/A'})"


class Problema:
    def __init__(self, acciones, estados, heuristica_h):
        self.acciones = acciones 
        self.estados = estados # dict de nombre -> objeto Estado
        self.heuristica_h = heuristica_h

    def obtener_vecinos(self, estado_actual):
        vecinos = []
        if estado_actual.nombre in self.acciones:
            nombres_vecinos = self.acciones[estado_actual.nombre].values()
            for nombre in nombres_vecinos:
                if nombre in self.estados:
                    vecinos.append(self.estados[nombre])
        # Asegurarse de no devolver vecinos duplicados si el mapa lo permite
        return list(set(vecinos)) 

    def evaluar(self, estado):
        """
        Función de evaluación (costo). Queremos minimizar esto.
        Devuelve el valor h(n) del estado.
        """
        return self.heuristica_h.get(estado.nombre, float('inf'))


# --- Algoritmo de Búsqueda de Haz Local ---

def busqueda_haz_local(problema, k, max_iteraciones):
    """
    Realiza la Búsqueda de Haz Local (Local Beam Search).
    - k: Ancho del haz (cuántos estados mantener)
    """
    
    # 1. Iniciar con k estados aleatorios únicos
    # Usamos random.sample para asegurar que sean únicos
    mejores_haces = random.sample(list(problema.estados.values()), k)
    
    # Rastrear la mejor solución global encontrada
    mejor_solucion_global = min(mejores_haces, key=lambda e: problema.evaluar(e))
    mejor_evaluacion_global = problema.evaluar(mejor_solucion_global)
    
    print(f"Iniciando con k={k} haces. Mejor inicial: {mejor_solucion_global.nombre} (h={mejor_evaluacion_global})")

    for i in range(max_iteraciones):
        # 2. Generar TODOS los vecinos de TODOS los k haces
        todos_los_vecinos = []
        for estado_haz in mejores_haces:
            todos_los_vecinos.extend(problema.obtener_vecinos(estado_haz))
            
        if not todos_los_vecinos:
            break # No hay más vecinos que explorar

        # 3. Eliminar duplicados (un vecino puede ser alcanzado por dos haces)
        todos_los_vecinos = list(set(todos_los_vecinos))
        
        # 4. Evaluar y ordenar la lista completa de vecinos
        todos_los_vecinos.sort(key=lambda estado: problema.evaluar(estado))
        
        # 5. Seleccionar los k mejores como los nuevos haces
        mejores_haces = todos_los_vecinos[:k]
        
        # 6. Actualizar la mejor solución global
        mejor_haz_actual = mejores_haces[0]
        evaluacion_mejor_haz = problema.evaluar(mejor_haz_actual)
        
        if evaluacion_mejor_haz < mejor_evaluacion_global:
            mejor_solucion_global = mejor_haz_actual
            mejor_evaluacion_global = evaluacion_mejor_haz
            print(f"  Iter {i}: ¡Nueva mejor sol. global! {mejor_solucion_global.nombre} (h={mejor_evaluacion_global})")
    
    return mejor_solucion_global


# --- Ejecución del Problema ---

# Variable global temporal para que __repr__ funcione (es un truco de depuración)
_problema_global_temp = None

if __name__ == "__main__":
    
    # 1. Definiciones (Igual que en Tabú, todo en minúsculas)
    
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
        'boomon': {'N': 'goorum', 'SO': 'kuart'}, # Óptimo local
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
    _problema_global_temp = problema_optimizacion # Asignar al 'truco' de depuración

    # Parámetros de Búsqueda de Haz Local
    K_HAZ = 3 # Usaremos 3 "haces" o "escaladores"
    MAX_ITERACIONES = 50

    print(f"\n--- Resolviendo (Encontrar mejor estado) con Búsqueda de Haz Local ---")
    solucion = busqueda_haz_local(problema_optimizacion, K_HAZ, MAX_ITERACIONES)
    
    print("\n--- Búsqueda finalizada ---")
    print(f"La mejor solución global encontrada fue: {solucion.nombre}")
    print(f"Valor de evaluación (h(n)): {problema_optimizacion.evaluar(solucion)}")