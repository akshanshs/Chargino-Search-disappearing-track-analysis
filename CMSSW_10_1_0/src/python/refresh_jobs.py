import os, sys
from glob import glob
try: filenames = sys.argv[1]
except: filenames = 'Run2016*.sh.e*'

filelist = glob(filenames)

for ifname, fname in enumerate(filelist):
    identifer = fname[:fname.rfind('.sh.e')]
    command = 'rm '+identifer+'*'
#    print command
    
    os.system(command)
