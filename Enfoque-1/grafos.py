# %% Acccion
class Accion:
    def __init__(self, nombre):
        self.nombre = nombre

def __str__(self):
    return self.nombre

# %% Estado
class Estado:
    def __init__(self, nombre, acciones):
        self.nombre = nombre
        self.acciones = acciones
    
    def __str__(self):
        return self.nombre

# %% Problema
class Problema:
    def __init__(self, estado_inicial, estados_objetivo, acciones):
        self.estado_inicial = estado_inicial
        self.estados_objetivo = estados_objetivo
        self.acciones = acciones

    def __str__(self):
        msg = "Estado Inicial: {0} -> Objetivos: {1} "
        return msg.format(self.estado_inicial, self.estados_objetivo)
    def es_objetivo(self, estado):
        return estado in self.estados_objetivo
    def resultado(self, estado, accion): ## Devuelve el estado resultado de aplicar la accion al estado
        if estado.nombre not in self.acciones.keys():
            return None
        acciones_estado = self.acciones[estado.nombre]
        if accion.nombre not in acciones_estado.keys():
            return None
        return acciones_estado[accion.nombre] ## Devuelve el estado resultado
    
# %% Nodo
class Nodo:
        