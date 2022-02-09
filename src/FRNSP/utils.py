from typing import Callable, Tuple, List, Dict
from neurons.neuron import Neuron


syn_type = Dict[Neuron, List[Tuple[List[Neuron], Callable[[int], int]]]]

def calculate_maximum_depth(syn, IN, OUT) -> int:    
    depths = [maximum_depth_path(syn, path, OUT) for node in IN for (path, f) in syn[node]]
    return max(depths) +1


def maximum_depth_path(syn: syn_type ,path: Neuron ,OUT: List[Neuron]) -> int:
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


def calculate_OUT(syn: syn_type, neurons: List[Neuron]) -> List[Neuron]:
    keys = list(syn.keys())
    res = []
    for neuron in neurons:
        if neuron not in keys:
            res.append(neuron)
    return res


