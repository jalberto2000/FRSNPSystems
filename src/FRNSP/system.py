from neurons.neuron import RuleNeuron, PropositionNeuron
from file_interpreter.parser import Parser
from file_interpreter.lexer import Lexer
from FRNSP.utils import calculate_IN, calculate_OUT, calculate_maximum_depth
import graphviz
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
        print(calculate_maximum_depth(self.syn, calculate_IN(self.syn), calculate_OUT(self.syn, self.neurons)))
    
    def plot_graph(self) -> None:
        graph = graphviz.Digraph(strict=True)
        p = len(self.propositions)
        for neuron in self.neurons:
            if type(neuron) == RuleNeuron:
                graph.node(str(neuron.id), label = 'R'+str(neuron.id-p))
            else:
                graph.node(str(neuron.id), label = 'P'+str(neuron.id))
        for key in self.syn:
            n1 = str(key.id)
            for (n2, f) in self.syn[key]:
                n2 = str(n2.id)
                
                if f(1) != 1:
                    graph.edge(n1, n2, penwidth = "2")
                else:
                    graph.edge(n1, n2)
                    
                
        graph.format = "svg"
        graph.render(directory='./test')

    def next_iteration(self) -> None:
        pass



    
