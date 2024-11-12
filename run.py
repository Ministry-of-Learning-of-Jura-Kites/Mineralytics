import sys
import os 
import subprocess
dirname = os.path.dirname(os.path.realpath(__file__))
subprocess.run(['python','-m',sys.argv[1].split(dirname)[1].replace('/','.').removesuffix(".py").removeprefix(".")])