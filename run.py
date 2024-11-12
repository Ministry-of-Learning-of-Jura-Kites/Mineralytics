import sys
import os 
import subprocess
dirname = os.path.dirname(os.path.realpath(__file__))
target_path = sys.argv[1]
target_path = os.path.relpath(target_path,dirname)
subprocess.run(['python','-m',target_path.replace('/','.').removesuffix(".py").removeprefix(".")])