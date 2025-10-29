import random

# --- Parámetros del Algoritmo Genético ---
TAMANO_POBLACION = 50
LONGITUD_CROMOSOMA = 20 # Cuántos bits tiene cada individuo
PROBABILIDAD_MUTACION = 0.01 # 1% de probabilidad de mutar un bit
PROBABILIDAD_CRUCE = 0.7   # 70% de probabilidad de cruzar dos padres
TAMANO_TORNEO = 3         # Para la selección
NUM_GENERACIONES = 100

# --- 1. Definición del Individuo ---
class Individuo:
    def __init__(self, cromosoma):
        # El "cromosoma" es la lista de bits (la solución candidata)
        self.cromosoma = cromosoma
        # La "aptitud" es qué tan buena es esta solución
        self.aptitud = 0

    def __repr__(self):
        return f"Cromosoma: {''.join(map(str, self.cromosoma))} | Aptitud: {self.aptitud}"

# --- 2. Funciones del AG ---

def crear_poblacion_inicial():
    """Crea la población de individuos aleatorios."""
    poblacion = []
    for _ in range(TAMANO_POBLACION):
        # Crea un cromosoma aleatorio (lista de 0s y 1s)
        cromosoma = [random.randint(0, 1) for _ in range(LONGITUD_CROMOSOMA)]
        poblacion.append(Individuo(cromosoma))
    return poblacion

def evaluar_poblacion(poblacion):
    """Calcula la aptitud de cada individuo (Problema OneMax)."""
    for individuo in poblacion:
        # La aptitud es simplemente la suma de los '1's
        individuo.aptitud = sum(individuo.cromosoma)

def seleccion_por_torneo(poblacion):
    """
    Selecciona un padre usando "selección por torneo".
    Es un método común y simple.
    """
    # 1. Elige k (TAMANO_TORNEO) individuos al azar de la población
    torneo = random.sample(poblacion, TAMANO_TORNEO)
    
    # 2. El individuo con la aptitud MÁS ALTA en ese grupo gana
    ganador = max(torneo, key=lambda individuo: individuo.aptitud)
    return ganador

def cruce_punto_unico(padre1, padre2):
    """
    Crea dos hijos a partir de dos padres usando cruce de un solo punto.
    """
    if random.random() < PROBABILIDAD_CRUCE:
        # Elige un punto de corte aleatorio
        punto_corte = random.randint(1, LONGITUD_CROMOSOMA - 1)
        
        # Crear hijos
        cromo_hijo1 = padre1.cromosoma[:punto_corte] + padre2.cromosoma[punto_corte:]
        cromo_hijo2 = padre2.cromosoma[:punto_corte] + padre1.cromosoma[punto_corte:]
        
        return Individuo(cromo_hijo1), Individuo(cromo_hijo2)
    else:
        # Si no hay cruce, los hijos son clones de los padres
        return Individuo(padre1.cromosoma), Individuo(padre2.cromosoma)

def mutacion_flip_bit(individuo):
    """
    Recorre cada "gen" (bit) y lo voltea con una baja probabilidad.
    """
    for i in range(LONGITUD_CROMOSOMA):
        if random.random() < PROBABILIDAD_MUTACION:
            # Voltear el bit
            individuo.cromosoma[i] = 1 - individuo.cromosoma[i] # (1->0, 0->1)

# --- 3. El Algoritmo Genético Principal ---

def algoritmo_genetico():
    
    # --- 1. Inicialización ---
    poblacion = crear_poblacion_inicial()
    evaluar_poblacion(poblacion)
    
    mejor_global = max(poblacion, key=lambda ind: ind.aptitud)
    print(f"Generación 0: Mejor aptitud = {mejor_global.aptitud}")
    
    for generacion in range(NUM_GENERACIONES):
        nueva_poblacion = []
        
        # Mantener al mejor individuo (Elitismo)
        # Esto asegura que la aptitud nunca disminuya
        nueva_poblacion.append(mejor_global)

        # --- 2. Creación de la Nueva Generación ---
        while len(nueva_poblacion) < TAMANO_POBLACION:
            # --- 3. Selección ---
            padre1 = seleccion_por_torneo(poblacion)
            padre2 = seleccion_por_torneo(poblacion)
            
            # --- 4. Cruce ---
            hijo1, hijo2 = cruce_punto_unico(padre1, padre2)
            
            # --- 5. Mutación ---
            mutacion_flip_bit(hijo1)
            mutacion_flip_bit(hijo2)
            
            nueva_poblacion.extend([hijo1, hijo2])

        # Asegurarse de que la población tenga el tamaño correcto
        poblacion = nueva_poblacion[:TAMANO_POBLACION]
        
        # --- 6. Evaluación ---
        evaluar_poblacion(poblacion)
        
        # Actualizar el mejor global
        mejor_actual = max(poblacion, key=lambda ind: ind.aptitud)
        if mejor_actual.aptitud > mejor_global.aptitud:
            mejor_global = mejor_actual
            print(f"Generación {generacion + 1}: ¡Nueva mejor aptitud! = {mejor_global.aptitud}")

        # Condición de parada (¡encontramos el óptimo!)
        if mejor_global.aptitud == LONGITUD_CROMOSOMA:
            print(f"¡Óptimo encontrado en la generación {generacion + 1}!")
            break
            
    return mejor_global

# --- Ejecución del Problema ---

if __name__ == "__main__":
    
    print(f"--- Resolviendo OneMax (Longitud={LONGITUD_CROMOSOMA}) con Algoritmo Genético ---")
    
    solucion = algoritmo_genetico()
    
    print("\n--- Búsqueda finalizada ---")
    print(f"La mejor solución global encontrada fue:")
    print(solucion)