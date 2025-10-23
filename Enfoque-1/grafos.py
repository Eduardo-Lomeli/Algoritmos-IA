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
    def __init__(self, estado, accion=None, acciones=None, padre=None):
           self.estado = estado
           self.accion = accion
           self.acciones = acciones
           self.padre = padre
        
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
                estado_hijo = problema.resultado(self.estado, accion_hijo)
                
                