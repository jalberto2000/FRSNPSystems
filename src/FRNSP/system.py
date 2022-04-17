from neurons.neuron import RuleNeuron, PropositionNeuron
from file_interpreter.parser import Parser
from file_interpreter.lexer import Lexer
from training_file_interpreter.lexer_training import LexerTraining
from training_file_interpreter.parser_training import ParserTraining
from FRNSP.utils import calculate_IN, calculate_OUT, calculate_maximum_depth, calculate_presyn, get_edge, Stack
import graphviz
import copy
from typing import Tuple, List
import random

class System():
    def __init__(self, file) -> None:
        lexer = Lexer()
        lexer.build()
        parser = Parser()
        parser.build(lexer)
        try:
            f = open(file, 'r', encoding= "utf8")
            self.propositions, self.rules = parser.parsing(f)
            f.close()
        except FileNotFoundError:
            print("La ruta introducida es incorrecta, abortando ejecucion")
            exit()
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

    def reset_system(self) -> None: #LLEVAMOS EL SISTEMA A UN ESTADO INICIAL PARA VOLVER A COMENZAR LA EJECUCION
        self.t = 0
        for neuron in self.neurons:
            if neuron not in self.IN:
                neuron.ready_to_fire = False

    def run_algorithm(self) -> Tuple[int, str]: #EJECUTAMOS EL ALGORITMO GUARDANDO EL ESTADO DE LA RED EN CADA PASO
        while(self.t < self.maximum_depth):
            self.next_iteration()
            self.plot_graph()
        index_of_neuron = self.neurons.index(max(self.OUT, key = lambda x : x.pulse_value))
        return (index_of_neuron+1,self.propositions[index_of_neuron][0])
        
    def run_algorithm_not_graph(self) -> Tuple[int, str]: #EJECUTAMOS EL ALGORITMO SIN GUARDAR EL ESTADO DE LA RED
        while(self.t < self.maximum_depth):
            self.next_iteration() 
        index_of_neuron = self.neurons.index(max(self.OUT, key = lambda x : x.pulse_value))
        return (index_of_neuron+1,self.propositions[index_of_neuron][0])
    def train_network(self, file: str) -> None:
        lexer = LexerTraining()
        lexer.build()
        parser = ParserTraining()
        parser.build(lexer)
        training_data = []
        try:
            f = open(file, 'r', encoding= "utf8")
            training_data = parser.parsing(f)
            f.close()
        except FileNotFoundError:
            print("La ruta introducida es incorrecta, abortando ejecucion")
            exit()
        self.training_algorithm(training_data)

    def training_algorithm(self, set: List[Tuple[List[Tuple[str, float]], str]]) -> None:
        def get_rule_neurons_involved(n, syn, IN):
            r_neurons = []
            st = Stack()
            st.push(n)
            while not st.is_empty(): #MIENTRAS HAYA ELEMENTOS EN LA PILA, COMPROBAMOS SUS ANTECEDENTES
                actual = st.get_element()
                for s in syn:
                    for p_n, f in syn[s]:
                        if actual == p_n:
                            if s not in IN: #SI NO ES UNA NEURONA DE ENTRADA LA INTRODUCIMOS EN LA PILA
                                st.push(s)
                            if type(s) == RuleNeuron: #SI ES UNA NEURONA DE REGLA LA GUARDAMOS
                                r_neurons.append(s)
            return r_neurons
        random.shuffle(set)
        training_set = set[0: int(0.7*len(set))]
        test_set = set[int(0.7*len(set)) : len(set)]

        for x in training_set:
            n_in, n_out = x
            for n, v in n_in: #PONEMOS LOS VALORES DE ENTRADA CORRESPONDIENTES
                self.neurons[n-1].pulse_value = v
            o_out, _ = self.run_algorithm_not_graph()
            
            if o_out != n_out:
                v_ex = self.neurons[n_out-1].pulse_value
                self.OUT.sort(key = lambda x : x.pulse_value)
                m_value = self.OUT[-1].pulse_value
                for n in self.OUT: 
                    
                    '''
                    PARA CADA NEURONA DE SALIDA, SI SU VALOR ES MAYOR QUE EL DE LA NEURONA ESPERADA, MODIFICAMOS EL FACTOR DE CONFIANZA
                    DE LAS NEURONAS DE REGLA IMPLICADAS
                    '''
                    if n.pulse_value > v_ex:
                        r_neurons = get_rule_neurons_involved(n, self.syn, self.IN)
                        for r_n in r_neurons: #MODIFICAMOS LAS NEURONAS IMPLICADAS
                            r_n.confidence_factor -= (n.pulse_value - v_ex)*0.01
                            if r_n.confidence_factor < 0:
                                r_n.confidence_factor = 0
                #MODIFICAMOS AHORA LAS NEURONAS IMPLICADAS EN LA NEURONA ESPERADA COMO RESULTADO
                r_neurons = get_rule_neurons_involved(self.neurons[n_out-1], self.syn, self.IN)
                for r_n in r_neurons:
                    r_n.confidence_factor += (m_value - v_ex) * 0.02
                    if r_n.confidence_factor > 1:
                        r_n.confidence_factor = 1
            self.reset_system() #VOLVEMOS EL SISTEMA A UN ESTADO INICIAL PARA PODER REALIZAR OTRA EJECUCION
        #COMPROBAMOS EL % DE ACIERTOS CON EL SET DE TEST    
        res = {True:0, False:0}
        cont = 0
        for y in test_set:
            n_in, n_out = y
            for n, v in n_in:
                self.neurons[n-1].pulse_value = v
            o_out, _ = self.run_algorithm_not_graph()
            if n_out == o_out:
                cont += 1
                res[True] += 1
            else:
                res[False] += 1
            self.reset_system()
        for r in self.neurons:
            if type(r) == RuleNeuron:
                print(r.confidence_factor)
        print("Hay un {}% de aciertos".format(int(100*(res[True]/len(test_set)))))
        print("Hay un {}% de fallos".format(int(100*(res[False]/len(test_set)))))
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
    