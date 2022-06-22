import argparse
from FRNSP.system import System
import os, shutil
parser = argparse.ArgumentParser()

parser.add_argument('-s', '--system', help = "File describing the system", type = str, required = True)
grupo = parser.add_mutually_exclusive_group(required = True)
grupo.add_argument('-e', '--exec', help = "File with initial values of neurons", type = str)
grupo.add_argument('-t', '--testing', type = str, help = "File describing range values for neurons")
grupo.add_argument('-l', '--learning', type = str, help = "Training file")
parser.add_argument('-od', '--output_dir', type = str, help = "Path of the folder where to save the results", required=True)

args = parser.parse_args()
output = args.output_dir
sys = args.system
if os.path.isdir(output):
    for filename in os.listdir(output): #RUTINA PARA ELIMINAR TODO EL CONTENIDO EN UN DIRECTORIO
        file_path = os.path.join(output, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    s = System(sys, output)
s.buildSystem()
if args.exec != None:
    exec = args.exec
    s.execute_system(exec, output)
elif args.testing != None:
    testing = args.testing
    s.test_system(testing)
elif args.learning != None:
    learning = args.learning
    s.train_network(learning)
else:
    raise Exception("La ruta introducida no es un directorio existente")










