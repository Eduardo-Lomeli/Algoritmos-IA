import random

# --- Clases de Estado y Problema (Igual que antes) ---
# Usaremos 'Estado' para representar las percepciones
class Estado:
    def __init__(self, nombre):
        self.nombre = nombre
    def __eq__(self, other):
        return isinstance(other, Estado) and self.nombre == other.nombre
    def __hash__(self):
        return hash(self.nombre)
    def __repr__(self):
        return f"Estado({self.nombre})"

# --- 1. El Entorno (El "Mundo Real" que el Agente NO conoce) ---
class Entorno:
    def __init__(self, acciones, estados):
        self._acciones_reales = acciones
        self._estados_reales = estados
    
    def obtener_percepcion_acciones(self, estado):
        """
        El agente "ve" qué acciones puede tomar desde donde está.
        """
        if estado.nombre in self._acciones_reales:
            return list(self._acciones_reales[estado.nombre].keys())
        return []
        
    def tomar_accion(self, estado_actual, nombre_accion):
        """
        El agente se mueve. El entorno le devuelve el nuevo estado.
        """
        if estado_actual.nombre in self._acciones_reales:
            if nombre_accion in self._acciones_reales[estado_actual.nombre]:
                nombre_destino = self._acciones_reales[estado_actual.nombre][nombre_accion]
                return self._estados_reales[nombre_destino]
        return estado_actual # Si la acción falla, se queda en el lugar


# --- 2. El Agente (El "Robot" que aprende) ---
class AgenteOnlineDFS:
    def __init__(self, estado_objetivo):
        self.objetivo = estado_objetivo
        self.estado_actual = None
        self.mapa_aprendido = {}     # Mapa de (estado, accion) -> estado_destino
        self.acciones_no_intentadas = {} # dict de estado -> lista de acciones
        self.pila_backtrack = []      # (estado_previo, accion_inversa)
        self.costo_total = 0

    def decidir_accion(self, percepcion_estado, percepcion_acciones):
        """
        El cerebro del agente. Decide qué acción tomar.
        """
        self.estado_actual = percepcion_estado
        
        if self.estado_actual == self.objetivo:
            return None # ¡Objetivo encontrado!

        # Si es un estado nuevo, registrar sus acciones
        if self.estado_actual not in self.acciones_no_intentadas:
            self.acciones_no_intentadas[self.estado_actual] = percepcion_acciones
            self.mapa_aprendido[self.estado_actual] = {}
        
        # --- Lógica DFS ---
        # Caso 1: Hay acciones que no hemos intentado desde aquí
        if self.acciones_no_intentadas[self.estado_actual]:
            accion = self.acciones_no_intentadas[self.estado_actual].pop()
            
            # Guardar cómo deshacer este movimiento
            # (Simplificación: asumimos que podemos encontrar el inverso)
            self.pila_backtrack.append(self.estado_actual)
            return accion
        
        # Caso 2: Callejón sin salida. Debemos retroceder (backtrack).
        if self.pila_backtrack:
            estado_previo = self.pila_backtrack.pop()
            
            # Encontrar la acción que nos lleva de vuelta
            for estado, acciones in self.mapa_aprendido.items():
                for acc, destino in acciones.items():
                    if estado == estado_previo and destino == self.estado_actual:
                        # ¡Encontrado! El 'estado_previo' es a donde queremos ir.
                        # Pero, ¿qué acción nos lleva allí desde 'self.estado_actual'?
                        # Esto es difícil en Búsqueda Online.
                        
                        # --- Lógica de Agente LRTA* (más simple) ---
                        # Olvidemos el backtracking de DFS, es complejo online.
                        # Simplemente tomemos una acción aleatoria
                        pass 
            
            # --- Simplifiquemos la lógica (Random Walk) ---
            # Un agente online real es más complejo (ej. LRTA*)
            # Este agente solo explorará aleatoriamente
            if percepcion_acciones:
                return random.choice(percepcion_acciones)
        
        # Fallo si no hay acciones y no hay backtrack
        return None # Atascado

    def aprender(self, estado_origen, accion, estado_destino):
        """
        Actualiza el mapa interno del agente.
        """
        if estado_origen not in self.mapa_aprendido:
             self.mapa_aprendido[estado_origen] = {}
        self.mapa_aprendido[estado_origen][accion] = estado_destino
        self.costo_total += 1 # Asumimos costo 1 por movimiento
        

# --- 3. Simulación ---
if __name__ == "__main__":
    
    # 1. Definiciones (El "Mundo Real")
    lanoi = Estado("lanoi"); nohoi = Estado("nohoi"); ruun = Estado("ruun")
    milos = Estado("milos"); ghiido = Estado("ghiido"); kuart = Estado("kuart")
    boomon = Estado("boomon"); goorum = Estado("goorum"); shiphos = Estado("shiphos")
    nokshos = Estado("nokshos"); pharis = Estado("pharis"); khamin = Estado("khamin")
    tarios = Estado("tarios"); peranna = Estado("peranna"); khandan = Estado("khandan")
    tawa = Estado("tawa"); theer = Estado("theer"); roria = Estado("roria"); kosos = Estado("kosos")

    acciones = {
        'lanoi': {'NE': 'nohoi', 'SO': 'lanoi', 'NO': 'ruun'},
        # ... (el resto del mapa) ...
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
    
    # 2. Configurar Simulación
    entorno = Entorno(acciones, estados)
    agente = AgenteOnlineDFS(estado_objetivo=kosos)
    
    estado_actual_agente = lanoi # Donde "despierta" el agente
    max_pasos = 200

    print(f"--- Simulación de Búsqueda Online (Objetivo: {kosos.nombre}) ---")
    print(f"Agente inicia en: {estado_actual_agente.nombre}")

    for i in range(max_pasos):
        # 1. El agente percibe su entorno
        acciones_posibles = entorno.obtener_percepcion_acciones(estado_actual_agente)
        
        # 2. El agente decide qué hacer
        accion_elegida = agente.decidir_accion(estado_actual_agente, acciones_posibles)
        
        if accion_elegida is None:
            if agente.estado_actual == agente.objetivo:
                print(f"\n¡ÉXITO! Objetivo encontrado en {i} pasos.")
                print(f"Costo total del viaje: {agente.costo_total}")
            else:
                print(f"\nFALLO. Agente atascado o se rindió.")
            break
            
        # 3. El entorno ejecuta la acción y devuelve el nuevo estado
        estado_origen = estado_actual_agente
        estado_destino = entorno.tomar_accion(estado_origen, accion_elegida)
        
        # 4. El agente aprende de la experiencia
        agente.aprender(estado_origen, accion_elegida, estado_destino)
        estado_actual_agente = estado_destino # El agente se movió físicamente
        
        print(f"Paso {i}: {estado_origen.nombre} --({accion_elegida})--> {estado_destino.nombre}")
        
    if i == max_pasos - 1:
        print("\nLímite de pasos alcanzado.")
        
    print("\n--- Mapa aprendido por el agente: ---")
    for origen, conecciones in agente.mapa_aprendido.items():
        for accion, destino in conecciones.items():
            print(f"  {origen.nombre} --({accion})--> {destino.nombre}")