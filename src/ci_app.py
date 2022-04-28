import argparse
from FRNSP.system import System
parser = argparse.ArgumentParser()

parser.add_argument('-s', '--system', help = "File describing the system", type = str, required = True)
grupo = parser.add_mutually_exclusive_group(required = True)
grupo.add_argument('-e', '--exec', help = "File with initial values of neurons", type = str, required = True)
grupo.add_argument('-t', '--testing', type = str, help = "File describing range values for neurons")
grupo.add_argument('-l', '--learning', type = str, help = "Training file")
parser.add_argument('-of', '--output_file', type = str, help = "Path of the folder where to save the results", required=True)

args = parser.parse_args()

sys = args.system

if args.testing != None:
    testing = args.testing
elif args.learning != None:
    learning = args.learning

output = args.output_file


s = System(sys)
s.buildSystem()



