import os, sys
from glob import glob
from time import sleep
try: filenames = sys.argv[1]
except: filenames = 'Run2016*.sh'

cwd = os.getcwd()
filelist = glob(filenames)
n = len(filelist)
for ifname, fname in enumerate(filelist):

    command = 'condor_qsub -cwd '+fname+' &'
    print command
    
    os.system(command)
    sleep(0.05)
#    if n < 50: sleep(0.5)
