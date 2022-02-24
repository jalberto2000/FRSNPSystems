import re, random
from FRNSP.system import System
NEURON_PATTERN = re.compile("P[0-9]+")
N_EJECUCIONES = 100

def get_execution_mode() -> int:
    print("¿Que operacion quiere realizar?")
    mode = 0
    while True:
        mode = input("(1) Ejecutar el sistema / (2) Testear el sistema para distintos valores de entrada: ")

        if (mode != "1") and (mode != "2"):
            print("El valor introducido no es correcto, por favor introduce un valor correcto")
        else:
            return mode

print("Bienvenido al modulo de simulacion de sistemas FRSNP")
file = input("Introduzca la ruta absoluta del archivo a partir del cual construir el sistema: ")

s = System(file)
s.buildSystem()
mode = get_execution_mode()
if int(mode) == 1:
    err = s.run_algorithm()
    print(err)
else:
    ids_in = [x.id for x in s.IN]
    ids_input = []
    while True:
        ids_input = []
        neurons_check = True
        neurons = input("Introduzca las neuronas del conjunto de entrada que van a ser variables separadas por espacios, si todas van a serlo no introduzca nada: ")
        if not neurons or neurons.isspace():
            ids_input = ids_in
        else:
            neurons = neurons.split(" ")
            
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
                    r1 = -1
                    r2 = -1
                    if len(rango) != 2:
                        print("El rango introducido no es valido")
                    else:
                        try:
                            r1 = float(rango[0])
                            r2 = float(rango[1])
                            bad_input = False
                        except:
                            print("El rango introducido no es valido")
                    if not r1 or not r2 or 1 < r1 < 0 or 1 < r2 < 0 or r1 > r2:
                        print("El rango de introducido no es valido") 
                        bad_input = True
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
                else:
                    bad_input = False
            
            sol = {}
            for _ in range(N_EJECUCIONES): #EJECUTAR LOS TESTS CON LOS RANGOS DETERMINADOS POR EL USUARIO
                s.reset_system()
                valores = []
                for id, r in zip(ids_input, rangos):
                    r = random.uniform(r[0], r[1])
                    valores.append(r)
                    s.neurons[id-1].pulse_value = r
                err = s.run_algorithm_not_graph()
                if err in sol:
                    sol[err] += 1
                else:
                    sol[err] = 1
            
            for pr in sol:
                print("El fallo '{0}' ocurre un {1:.2f}% de las veces".format(pr, (100*(sol[pr]/N_EJECUCIONES))))

input("Introduzca cualquier valor para salir del programa")