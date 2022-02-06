from operator import truth
from neurons.neuron import RuleNeuron, PropositionNeuron
from file_interpreter.parser import Parser
from file_interpreter.lexer import Lexer
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
        self.graph = graphviz.Digraph()
        self.neurons = []
        self.syn = []
        print(self.rules)
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

        #SE CREAN LAS CONEXIONES CORRESPONDIENTES AL SISTEMA
        for i in range(len(self.rules)):
            nodes = self.rules[i][0]
            if len(nodes) == 2: #NOS ENCONTRAMOS ANTE UNA REGLA IF P THEN P
                n_1 = nodes[0]
                if '¬' in n_1:
                    n_1 = int(n_1[2:])
                else:
                    n_1 = int(n_1[1:])
                n_c =  nodes[1]
                if '¬' in n_c:
                    n_c = int(n_c[2:])
                else:
                    n_c = int(n_c[1:])
                self.syn.append((self.neurons[n_1-1], self.neurons[n_propositions+i+1]))
                self.syn.append((self.neurons[n_propositions+i+1], self.neurons[n_c-1]))
            else: #NOS ENCONTRAMOS ANTE UNA REGLA AND U OR
                n_c = nodes[-1]
                nodes = nodes[:-1]
                if '¬' in n_c:
                    n_c = int(n_c[2:])
                else:
                    n_c = int(n_c[1:])
                print(nodes[1:])
                for node in nodes[1:]:
                    n = node
                if '¬' in n:
                    n = int(n[2:])
                else:
                    n = int(n[1:])
                    self.syn.append((self.neurons[n-1], self.neurons[n_propositions+i+1]))
                    self.syn.append((self.neurons[n_propositions+i+1], self.neurons[n_c-1]))
        
        print(len(self.syn))

    
    def plot_graph(self):
        graph = graphviz.Digraph()
        p = len(self.propositions)
        for neuron in self.neurons:
            if type(neuron) == RuleNeuron:
                graph.node(str(neuron.id), label = 'R'+str(neuron.id-p))
            else:
                graph.node(str(neuron.id), label = 'P'+str(neuron.id))
        for (n1, n2) in self.syn:
            graph.edge(str(n1.id), str(n2.id))
        graph.format = "svg"
        graph.render(directory='./test')
        

    