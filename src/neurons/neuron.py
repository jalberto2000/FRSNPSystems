from typing import Callable

class Neuron():
    def __init__(self,id:int, function:Callable, ready_to_fire:bool = False, pulse_value:float = 0) -> None:
        self.ready_to_fire = ready_to_fire
        self.pulse_value = pulse_value
        self.function = function
        self.id = id
class PropositionNeuron(Neuron):
    def __init__(self, id:int, pulse_value:float = 0, truth_value: float = 0, ready_to_fire:bool = False) -> None:
        Neuron.__init__(self, id, function = max, ready_to_fire=ready_to_fire, pulse_value = pulse_value)
        self.truth_value = truth_value
        
class RuleNeuron(Neuron):
    def __init__(self, id:int, function: Callable, pulse_value:float = 0,  confidence_factor:float = 0, ready_to_fire:bool = False) -> None:
        Neuron.__init__(self, id, function = function, ready_to_fire=ready_to_fire, pulse_value = pulse_value)
        self.pulse_value = pulse_value
        self.confidence_factor = confidence_factor