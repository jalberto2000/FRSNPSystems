from typing import Callable, Tuple, List, Dict
from neurons.neuron import Neuron


syn_type = Dict[Neuron, List[Tuple[List[Neuron], Callable[[int], int]]]]

#FUNCIONES QUE CALCULAN LA PROFUNDIDAD MAXIMA DE LA RED 
def calculate_maximum_depth(syn: syn_type, IN: List[Neuron], OUT: List[Neuron]) -> int:    
    depths = [maximum_depth_path(syn, path, OUT) for node in IN for (path, f) in syn[node]]
    return max(depths) +1


def maximum_depth_path(syn: syn_type, path: Neuron, OUT: List[Neuron]) -> int:
    if path in OUT:
        return 0
    else:
        for (node, f) in syn[path]: 
            depths = [maximum_depth_path(syn, node, OUT)]
            depth = 1 + max(depths)
        return depth

#FUNCION QUE CALCULA EL CONJUNTO IN DEL SISTEMA
def calculate_IN(syn: syn_type) -> List[Neuron]:
    keys = list(syn.keys())
    values = list(syn.values())
    plain_values = []
    res = []
    for value in values:
        for (neuron, f) in value:
            plain_values.append(neuron)
    for key in keys:
        if key not in plain_values:
            res.append(key)
    return res

#FUNCION QUE CALCULA EL CONJUNTO OUT DE NEURONAS
def calculate_OUT(syn: syn_type, neurons: List[Neuron]) -> List[Neuron]:
    keys = list(syn.keys())
    res = []
    for neuron in neurons:
        if neuron not in keys:
            res.append(neuron)
    return res


#FUNCION QUE CALCULA EL PRESYN DE UNA NEURONA

def calculate_presyn(syn: syn_type, neuron: Neuron, IN: List[Neuron]) -> List[Neuron]:
    res = []
    if neuron in IN:
        return []
    else:
        for key in syn:
            possibles = syn[key]
            for (possible, f) in possibles:
                if neuron == possible:
                    res.append(key)
    return list(set(res))

def get_edge(syn: syn_type, n1: Neuron, n2: Neuron) -> Tuple[Neuron, Callable]:
    possibles = syn[n1]
    for (n, f) in possibles:
        if n == n2:
            return (n,f)
    return None

'''
UNA CLASE QUE IMPLEMENTA UNA ESTRUCTURA DE DATOS TIPO LIFO PARA SER USADA EN EL 
ALGORITMO DE APRENDIZAJE DEL SISTEMA
'''
class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value): #INSERTAR UN ELEMENTO
        self.stack.insert(0, value)
    def pop(self): #ELIMINAR EL PRIMER ELEMENTO SIN DEVOLVER SU VALOR
        self.stack.pop(0)
    def get_element(self): #OBTENER EL PRIMER ELEMENTO ELIMINANDOLO DE LA PILA
        return self.stack.pop(0)
    def is_empty(self) -> bool: #COMPROBAR SI LA PILA ESTA VACIA
        return len(self.stack) == 0
    

