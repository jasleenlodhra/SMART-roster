import os
import sys

mydir = os.getcwd()
mydir_tmp = mydir + "\\code"
mydir_new = os.chdir(mydir_tmp) 
os.system(f'python main.py {sys.argv[1]}')