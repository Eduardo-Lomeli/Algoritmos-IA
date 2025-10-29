# --- Definición del Problema (CSP) ---

# 1. Variables: Las regiones
variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']

# 2. Dominios: Los valores posibles para cada variable
dominios = {
    var: ['Rojo', 'Verde', 'Azul'] for var in variables
}

# 3. Restricciones: Qué regiones son adyacentes (no pueden tener el mismo color)
# (Usamos una lista de adyacencia)
restricciones = {
    'WA': ['NT', 'SA'],
    'NT': ['WA', 'SA', 'Q'],
    'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
    'Q': ['NT', 'SA', 'NSW'],
    'NSW': ['Q', 'SA', 'V'],
    'V': ['SA', 'NSW'],
    'T': [] # Tasmania no es adyacente a nadie
}

# --- Algoritmo de Búsqueda de Vuelta Atrás ---

def es_consistente(variable, valor, asignacion, restricciones):
    """
    Comprueba si una asignación (variable = valor) es consistente
    con las asignaciones ya hechas.
    """
    # Itera sobre los vecinos de la variable que estamos comprobando
    for vecino in restricciones[variable]:
        # Si el vecino ya está en la asignación...
        if vecino in asignacion:
            # ...y tiene el MISMO valor que estamos intentando poner...
            if asignacion[vecino] == valor:
                # ...¡entonces hay un conflicto!
                return False
    # Si no hubo conflictos con ningún vecino, es consistente
    return True

def seleccionar_variable_sin_asignar(variables, asignacion):
    """
    Encuentra la primera variable que aún no tiene valor.
    (Esta es la forma más simple, luego veremos formas más inteligentes)
    """
    for var in variables:
        if var not in asignacion:
            return var
    return None # Todas están asignadas

def backtracking_search(variables, dominios, restricciones, asignacion):
    """
    La función recursiva principal de backtracking.
    'asignacion' es un dict de {variable: valor}
    """
    
    # --- 1. Caso Base: ¿Está la solución completa? ---
    if len(asignacion) == len(variables):
        return asignacion # ¡Éxito!

    # --- 2. Seleccionar una variable para asignar ---
    var = seleccionar_variable_sin_asignar(variables, asignacion)
    
    # --- 3. Iterar sobre los valores del dominio ---
    for valor in dominios[var]:
        
        # --- 4. Comprobar restricciones ---
        if es_consistente(var, valor, asignacion, restricciones):
            
            # 5. Si es consistente, la "probamos" (move forward)
            asignacion[var] = valor
            
            # 6. Llamada recursiva para la siguiente variable
            resultado = backtracking_search(variables, dominios, restricciones, asignacion)
            
            # 7. Comprobar si la recursión tuvo éxito
            if resultado is not None:
                return resultado # ¡Propagar el éxito hacia arriba!
            
            # --- 8. ¡BACKTRACK! ---
            # Si 'resultado' fue None, significa que esta ruta falló.
            # Quitamos la asignación (retrocedemos) y probamos el siguiente valor.
            del asignacion[var]
            
    # Si el bucle termina, significa que ningún valor funcionó para esta variable
    return None # Fracaso

# --- Ejecución del Problema ---

if __name__ == "__main__":
    
    print("--- Resolviendo CSP de Coloreado de Mapa con Backtracking ---")
    
    # Iniciamos la búsqueda con una asignación vacía
    asignacion_inicial = {}
    solucion = backtracking_search(variables, dominios, restricciones, asignacion_inicial)
    
    if solucion:
        print("\n¡Solución encontrada!")
        for variable, valor in solucion.items():
            print(f"  {variable}: {valor}")
    else:
        print("\nNo se encontró solución.")