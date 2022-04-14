from neurons.neuron import RuleNeuron, PropositionNeuron
from file_interpreter.parser import Parser
from file_interpreter.lexer import Lexer
from FRNSP.utils import calculate_IN, calculate_OUT, calculate_maximum_depth, calculate_presyn, get_edge
import graphviz
import copy
class System():
    def __init__(self, file) -> None:
        self.lexer = Lexer()
        self.lexer.build()
        self.parser = Parser()
        self.parser.build(self.lexer)
        f = open(file, 'r', encoding= "utf8")
        self.propositions, self.rules = self.parser.parsing(f)
        f.close()
        self.t = 0
        self.graph = graphviz.Digraph()
        self.neurons = []
        self.syn = {}
        self.IN = []
        self.OUT = []
        self.maximum_depth = None
    def buildSystem(self) -> None:
        id = 1

        #SE CREAN LAS NEURONAS CORRESPONDIENTES A LAS PROPOSICIONES DEL SISTEMA
        for proposition in self.propositions:
            if len(proposition) == 3:
                neuron = PropositionNeuron(id, pulse_value = proposition[2],truth_value=proposition[2], ready_to_fire = True)
                self.neurons.append(neuron)
            else:
                neuron = PropositionNeuron(id)
                self.neurons.append(neuron)
            id += 1

        #SE CREAN LAS NEURONAS CORRESPONDIENTES A LAS REGLAS DEL SISTEMA
        for rule in self.rules:
            if rule[0][0] == 'AND':
                neuron = RuleNeuron(id, function= min, confidence_factor= rule[2])
                self.neurons.append(neuron)
            else:
                neuron = RuleNeuron(id, function= max, confidence_factor = rule[2])
                self.neurons.append(neuron)
            id += 1
        n_propositions = len(self.propositions) -1

        #CONEXIONES COMO DICCIONARIO LLAVE = NEURONA1 VALOR = (NEURONA2, FUNCION IDENTIDAD O INVERSA)
        for i in range(len(self.rules)):
            nodes = self.rules[i][0]
            neurona_regla = self.neurons[n_propositions+i+1]
            if len(nodes) == 2: #NOS ENCONTRAMOS ANTE UNA REGLA DE TIPO IF P THEN P
                n_1 = nodes[0]
                n_c = self.neurons[int(nodes[1][1:])-1]
                if '¬' in n_1: #LA CONEXION ES DE TIPO NOT, POR LO QUE LA FUNCION SERA LA INVERSA
                    n_1 = self.neurons[int(n_1[2:])-1]
                    if n_1 not in self.syn:
                        n_c = self.neurons[int(n_c[1:])-1]
                        self.syn[n_1] = [(neurona_regla, lambda x: 1-x)]

                    else:
                        self.syn[n_1].append((neurona_regla, lambda x: 1-x))
                    
                else: #LA CONEXION NO ES DE TIPO NOT, POR LO QUE LA FUNCION SERA LA IDENTIDAD
                    n_1 = self.neurons[int(n_1[1:])-1]
                    if n_1 not in self.syn:
                        self.syn[n_1] = [(neurona_regla, lambda x:x)]
                    else:
                        self.syn[n_1].append((neurona_regla, lambda x:x))
                if neurona_regla not in self.syn:
                    self.syn[neurona_regla] = [(n_c, lambda x: x)]
                else:
                    self.syn[neurona_regla].append((n_c, lambda x: x))
            else: #NOS ENCONTRAMOS ANTE UNA REGLA AND U OR
                n_c = self.neurons[int(nodes[-1][1:])-1]
                nodes = nodes[:-1]
                for node in nodes[1:]:
                    n_1 = node
                    if '¬' in n_1:
                        n_1 = self.neurons[int(n_1[2:])-1]
                        if n_1 not in self.syn:
                            self.syn[n_1] = [(neurona_regla, lambda x: 1-x)]
                        else:
                            self.syn[n_1].append((neurona_regla, lambda x:1-x))
                    else:
                        n_1 = self.neurons[int(n_1[1:])-1]
                        if n_1 not in self.syn:
                            self.syn[n_1] = [(neurona_regla, lambda x: x)]
                        else:
                            self.syn[n_1].append((neurona_regla, lambda x: x))
                    if neurona_regla not in self.syn:
                        self.syn[neurona_regla] = [(n_c, lambda x: x)]
                    else:
                        self.syn[neurona_regla].append((n_c, lambda x: x))
        self.IN = calculate_IN(self.syn)
        self.OUT = calculate_OUT(self.syn, self.neurons)
        self.maximum_depth = calculate_maximum_depth(self.syn, self.IN, self.OUT)

#FUNCION QUE COMPUTA LA SIGUIENTE ITERACION EN EL SISTEMA
    def next_iteration(self) -> None:
        next_it = []
        for neuron in self.neurons:
            if neuron in self.IN: #LA NEURONA PERTENECE AL CONJUNTO IN
                if self.t >= self.maximum_depth:
                    n_neuron = copy.copy(neuron)
                    n_neuron.truth_value = 0 
                    n_neuron.ready_to_fire = 0
                    next_it.append(n_neuron)
                else:
                    n_neuron = copy.copy(neuron)
                    next_it.append(n_neuron)
            else: #LA NEURONA NO PERTENECE AL CONJUNTO IN
                if not neuron.ready_to_fire:
                    presyn = calculate_presyn(self.syn, neuron, self.IN)
                    all_actives = True
                    for n in presyn:
                        if not n.ready_to_fire:
                            all_actives = False
                            break
                    if all_actives:
                        gs = []
                        for neuron_firing in presyn:
                            _,f =  get_edge(self.syn, neuron_firing, neuron)
                            if type(neuron_firing) == PropositionNeuron:
                                gs.append(f(neuron_firing.pulse_value))
                            else:
                                gs.append(f(neuron_firing.pulse_value)*neuron_firing.confidence_factor)
                        n_neuron = copy.copy(neuron)
                        n_neuron.pulse_value = n_neuron.function(gs)
                        n_neuron.ready_to_fire = True
                        next_it.append(n_neuron)
                    else:
                        n_neuron = copy.copy(neuron)
                        next_it.append(n_neuron)
                else:
                    n_neuron = copy.copy(neuron)
                    next_it.append(n_neuron)


        for i in range(len(self.neurons)):
            if type(self.neurons[i]) == PropositionNeuron:
                self.neurons[i].pulse_value = next_it[i].pulse_value
                self.neurons[i].ready_to_fire = next_it[i].ready_to_fire
                self.neurons[i].truth_value = next_it[i].truth_value
            else:
                self.neurons[i].ready_to_fire = next_it[i].ready_to_fire
                self.neurons[i].pulse_value = next_it[i].pulse_value
                self.neurons[i].confidence_factor = next_it[i].confidence_factor

        self.t += 1

    def run_algorithm(self) -> None:
        while(self.t < self.maximum_depth):
            self.next_iteration()
            self.plot_graph()

        maximum_output_neuron = max(self.OUT, key = lambda x : x.pulse_value)
        ind = self.neurons.index(maximum_output_neuron)
        print("El fallo mas probable es ->  %s" % self.propositions[ind])

    def plot_graph(self) -> None:
        graph = graphviz.Digraph(strict=True, graph_attr={"splines": "line"})
        p = len(self.propositions)
        for neuron in self.neurons:
            if type(neuron) == RuleNeuron:
                if neuron.ready_to_fire:
                    graph.node(str(neuron.id), label = str(round(neuron.pulse_value, 2)), xlabel = 'R'+str(neuron.id-p), style = "filled",fillcolor = "lightgray")
                else:
                    graph.node(str(neuron.id), label = str(round(neuron.pulse_value, 2)), xlabel = 'R'+str(neuron.id-p))
            else:
                if neuron.ready_to_fire:
                    graph.node(str(neuron.id), label = str(round(neuron.pulse_value, 2)), xlabel = 'P'+str(neuron.id), style = "filled", fillcolor = "lightgray")
                else:
                    graph.node(str(neuron.id), label = str(round(neuron.pulse_value, 2)), xlabel = 'P'+str(neuron.id))
        for key in self.syn:
            n1 = str(key.id)
            for (n2, f) in self.syn[key]:
                n2 = str(n2.id)
                
                if f(1) != 1:
                    graph.edge(n1, n2, penwidth = "2")
                else:
                    graph.edge(n1, n2)
        with graph.subgraph() as sg:
            sg.attr(rank = "min")
            for n in self.IN:
                sg.node(str(n.id))

        with graph.subgraph() as sg:
            sg.attr(rank = "max")
            for n in self.OUT:
                sg.node(str(n.id))
                 
        graph.format = "svg"
        graph.render(directory='./test/grafo%d' %self.t)
    