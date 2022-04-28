from email import parser
import re, random, os
from FRNSP.system import System
from neurons.neuron import RuleNeuron

sistema_1 = System("./test/sistema")
sistema_1.buildSystem()
archivo_aprendizaje_sistema_1 = "./test/training_sistema"
archivo_aprendizaje_sistema_2 = "./test/training_sistema2"
sistema_2 = System("./test/sistema2")
sistema_2.buildSystem()
with open('./test/output_data', 'a') as f:
    f.write("SISTEMA 1 \n")
for i in range(10):
    n_rule_value = {}
    for n in sistema_1.neurons:
        if type(n) == RuleNeuron:
            n.confidence_factor = random.random()
            n_rule_value[n.id] = n.confidence_factor    
    with open('./test/output_data', 'a') as f:
        s = "EJECUCION {} VALORES INICIALES \n".format(i)
        for k in n_rule_value:
            s += "REGLA {} -> {} \n".format(k, n_rule_value[k])
        f.write(s)
    sistema_1.train_network(archivo_aprendizaje_sistema_1)
    sistema_1.reset_system()

    with open('./test/output_data', 'a') as f:
        s = "VALORES FINALES \n".format(i)
        for k in n_rule_value:
            s += "REGLA {} -> {} \n".format(k, sistema_1.neurons[k-1].confidence_factor)
        f.write(s)
with open('./test/output_data', 'a') as f:
    f.write("SISTEMA 2 \n")
for i in range(10):
    n_rule_value = {}
    for n in sistema_2.neurons:
        if type(n) == RuleNeuron:
            n.confidence_factor = random.random()
            n_rule_value[n.id] = n.confidence_factor    
    with open('./test/output_data', 'a') as f:
        s = "EJECUCION {} VALORES INICIALES \n".format(i)
        for k in n_rule_value:
            s += "REGLA {} -> {} \n".format(k, n_rule_value[k])
        f.write(s)
    sistema_2.train_network(archivo_aprendizaje_sistema_2)

    with open('./test/output_data', 'a') as f:
        s = "VALORES FINALES \n".format(i)
        for k in n_rule_value:
            s += "REGLA {} -> {} \n".format(k, sistema_2.neurons[k-1].confidence_factor)
        f.write(s)