import random
import math

# --- Clases (Estado, Problema) ---
# (Idénticas a las usadas en Búsqueda Tabú)

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
        return vecinos

    def obtener_vecino_aleatorio(self, estado_actual):
        """
        Devuelve un único vecino aleatorio.
        """
        vecinos = self.obtener_vecinos(estado_actual)
        if vecinos:
            return random.choice(vecinos)
        return None

    def evaluar(self, estado):
        """
        Función de evaluación (costo). Queremos minimizar esto.
        Devuelve el valor h(n) del estado.
        """
        return self.heuristica_h.get(estado.nombre, float('inf'))


# --- Algoritmo de Temple Simulado ---

def temple_simulado(problema, temp_inicial, factor_enfriamiento, num_iteraciones):
    """
    Realiza la búsqueda por Temple Simulado.
    """
    
    # 1. Iniciar en un estado aleatorio
    estado_aleatorio = random.choice(list(problema.estados.values()))
    solucion_actual = estado_aleatorio
    evaluacion_actual = problema.evaluar(solucion_actual)
    
    # La mejor solución encontrada hasta ahora
    mejor_solucion_global = solucion_actual
    mejor_evaluacion_global = evaluacion_actual
    
    temperatura = temp_inicial
    
    print(f"Iniciando en: {solucion_actual.nombre} (h={evaluacion_actual}), Temp: {temperatura:.2f}")

    for i in range(num_iteraciones):
        if temperatura < 0.01: # Prácticamente congelado
            break
            
        # 2. Elegir un vecino aleatorio
        vecino = problema.obtener_vecino_aleatorio(solucion_actual)
        if vecino is None:
            continue

        # 3. Evaluar el vecino
        evaluacion_vecino = problema.evaluar(vecino)
        
        # 4. Decidir si moverse
        delta_energia = evaluacion_vecino - evaluacion_actual
        
        # Caso 1: El vecino es MEJOR (delta_energia < 0)
        if delta_energia < 0:
            solucion_actual = vecino
            evaluacion_actual = evaluacion_vecino
            # Actualizar el mejor global si es necesario
            if evaluacion_actual < mejor_evaluacion_global:
                mejor_solucion_global = solucion_actual
                mejor_evaluacion_global = evaluacion_actual
                print(f"  Iter {i}: ¡Mejor sol. global! {mejor_solucion_global.nombre} (h={mejor_evaluacion_global})")
        
        # Caso 2: El vecino es PEOR (delta_energia >= 0)
        # Aceptar con una probabilidad P = e^(-delta_E / T)
        else:
            probabilidad_aceptacion = math.exp(-delta_energia / temperatura)
            if random.random() < probabilidad_aceptacion:
                solucion_actual = vecino
                evaluacion_actual = evaluacion_vecino
                # print(f"  Iter {i}: Aceptado movimiento PEOR a {solucion_actual.nombre} (h={evaluacion_actual}) con T={temperatura:.2f}")

        # 5. Enfriar la temperatura
        temperatura *= factor_enfriamiento

    return mejor_solucion_global


# --- Ejecución del Problema ---

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

    # Parámetros de Temple Simulado
    TEMP_INICIAL = 100.0
    FACTOR_ENFRIAMIENTO = 0.99 # Enfriamiento lento
    NUM_ITERACIONES = 1000

    print(f"\n--- Resolviendo (Encontrar mejor estado) con Temple Simulado ---")
    solucion = temple_simulado(problema_optimizacion, TEMP_INICIAL, FACTOR_ENFRIAMIENTO, NUM_ITERACIONES)
    
    print("\n--- Búsqueda finalizada ---")
    print(f"La mejor solución global encontrada fue: {solucion.nombre}")
    print(f"Valor de evaluación (h(n)): {problema_optimizacion.evaluar(solucion)}")