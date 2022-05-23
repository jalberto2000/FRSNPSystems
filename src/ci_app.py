import argparse
from FRNSP.system import System
import os
parser = argparse.ArgumentParser()

parser.add_argument('-s', '--system', help = "File describing the system", type = str, required = True)
grupo = parser.add_mutually_exclusive_group(required = True)
grupo.add_argument('-e', '--exec', help = "File with initial values of neurons", type = str)
grupo.add_argument('-t', '--testing', type = str, help = "File describing range values for neurons")
grupo.add_argument('-l', '--learning', type = str, help = "Training file")
parser.add_argument('-od', '--output_dir', type = str, help = "Path of the folder where to save the results", required=True)

args = parser.parse_args()
output = args.output_dir
# for f in os.listdir(output):
#     os.remove(output+ '\\'+f)
sys = args.system

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










