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
    def __init__(self, estado_inicial, estados_objetivo, acciones, estados=None):
        self.estado_inicial = estado_inicial
        self.estados_objetivo = estados_objetivo
        self.acciones = acciones
        self.estados = estados if estados else {}

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
        nombre_estado_resultado = acciones_estado[accion.nombre]
        # Si estados está disponible, retornar el objeto Estado, sino retornar el nombre
        if self.estados and nombre_estado_resultado in self.estados:
            return self.estados[nombre_estado_resultado]
        return nombre_estado_resultado ## Devuelve el estado resultado
    
# %% Nodo
class Nodo:
    def __init__(self, estado, accion=None, acciones=None, padre=None):
           self.estado = estado
           self.accion = accion
           self.acciones = acciones
           self.padre = padre
           self.hijos = []
        
    def __str__(self):
            return self.estado.nombre
       
    def expandir(self, problema):
           self.hijos = []
           if not self.acciones:
               if self.estado.nombre in problema.acciones.keys():
                    return self.hijos
               self.acciones = problema.acciones[self.estado.nombre]
           for accion in self.acciones.keys():
                accion_hijo = Accion(accion)
                nuevo_estado = problema.resultado(self.estado, accion_hijo)
                acciones_nuevo = {}
                if nuevo_estado.nombre in problema.acciones.keys():
                    acciones_nuevo = problema.acciones[nuevo_estado.nombre]
                hijo = Nodo(nuevo_estado, accion_hijo, acciones_nuevo, self)
                self.hijos.append(hijo)
           return self.hijos