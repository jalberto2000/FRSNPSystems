import re, random
from FRNSP.system import System
NEURON_PATTERN = re.compile("P[0-9]+")
N_EJECUCIONES = 100
print("Bienvenido al modulo de simulacion de sistemas FRSNP")
file = input("Introduzca la ruta absoluta del archivo a partir del cual construir el sistema: ")

s = System(file)
s.buildSystem()
print("¿Que operacion quiere realizar?")

mode = 0
while True:
    mode = input("(1) Ejecutar el sistema / (2) Testear el sistema para distintos valores de entrada")

    if (mode != "1") and (mode != "2"):
        print("El valor introducido no es correcto, por favor introduce un valor correcto")
    else:
        break

if int(mode) == 1:
    err = s.run_algorithm()
    print(err)
    #TODO PRINTEAR LA SOLUCION Y TERMINAR EL PROGRAMA
else:
    ids_in = [x.id for x in s.IN]
    ids_input = []
    while True:
        ids_input = []
        neurons = input("Introduzca las neuronas del conjunto de entrada que van a ser variables separadas por espacios, si todas van a serlo no introduzca nada")
        if not neurons or neurons.isspace():
            pass
            #TODO TODAS LAS NEURONAS SON VARIABLES
        else:
            neurons = neurons.split(" ")
            neurons_check = True
            for neuron in neurons:

                if not NEURON_PATTERN.match(neuron):
                    print("Las neuronas introducidas son incorrectas, por favor introduzca valores correctos")
                    neurons_check = False
                    break
                else:
                    try:
                        neuron = int(neuron[1:])
                    except ValueError:
                        print("Las neuronas introducidas son incorrectas, por favor introduzca valores correctos")
                        neurons_check = False
                        break
                    if neuron not in ids_in:
                        print("Alguna de las neuronas introducidas no pertenece al conjunto de entrada")
                        neurons_check = False          
                        break
                    else:
                        ids_input.append(neuron)
        rangos = []
        if neurons_check:
            for id in ids_input: #RECIBIR LOS DATOS DE LOS RANGOS DE VARIABILIDAD
                bad_input = True
                while bad_input:
                    rango = input("Introduzca el rango de variabilidad de la neurona %d separado por un guion (entre 0.0 y 1.0) : " % id)
                    rango = rango.split("-")
                    if len(rango) != 2:
                        print("El rango introducido no es valido")
                    else:
                        try:
                            r1 = float(rango[0])
                            r2 = float(rango[1])
                            bad_input = False
                        except:
                            print("El rango introducido no es valido")
                    if 1 < r1 < 0 or 1 < r2 < 0:
                        print("El rango de introducido no es valido") 
                rangos.append((r1, r2))

            bad_input = True
            while bad_input:
                n = input("Introduzca el numero de tests a ejecutar, por defecto se ejecutarán 100: ")
                if not(n.isspace() or n == ""):
                    try:
                        N_EJECUCIONES = int(n)
                        bad_input = False
                    except:
                        print("El dato introducido no es correcto")
            
            for _ in range(N_EJECUCIONES): #EJECUTAR LOS TESTS CON LOS RANGOS DETERMINADOS POR EL USUARIO
                for id, r in zip(ids_input, rangos):
                    s.neurons[id-1].pulse_value = random.uniform(r[0], r[1])
                err = s.run_algorithm()
                print(err)