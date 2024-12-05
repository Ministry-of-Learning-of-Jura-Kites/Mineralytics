import sys
import os 
import subprocess

if __name__ == '__main__':
  dirname = os.path.dirname(os.path.realpath(__file__))
  target_path = sys.argv[1]
  target_path = os.path.relpath(target_path,dirname)
  if target_path==os.path.normpath("./run.py"):
    print("error: don't call this file to run itself!")
    exit(1)

  try:
    subprocess.run(["python",'-m',target_path.replace(os.path.sep,'.').removesuffix(".py").removeprefix(".")])
  except KeyboardInterrupt:
    pass
