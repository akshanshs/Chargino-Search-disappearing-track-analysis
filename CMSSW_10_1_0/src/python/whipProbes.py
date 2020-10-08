import os, sys
from glob import glob

try: analyzer = sys.argv[1]
except: analyzer = 'EXO-16-044_attempt.py'
analyzer = analyzer.replace('python/','')
    
try: filenames = sys.argv[2]
except: filenames = '/nfs/dust/cms/user/beinsam/LongLiveTheChi/aodsim/smallchunks/pMSSM12_MCMC1_10_374794_step2_AODSIM_*.root'

cwd = os.getcwd()
filelist = glob(filenames)

filesperjob = 15

def main():
    ijob = 1
    files = ''
    for ifname, fname in enumerate(filelist):
        files += fname+','
        if (ifname+1)%filesperjob==filesperjob-1:
            jobname = fname[fname.rfind('/')+1:].replace('.root','_'+str(ijob))
            fjob = open('bird/'+jobname+'.sh','w')
            files = files[:-1]
            fjob.write(jobscript.replace('CWD',cwd).replace('INFILE',files).replace('ANALYZER',analyzer))
            fjob.close()
            os.chdir('bird')
            command = 'condor_qsub -cwd '+jobname+'.sh &'
            print command
            os.system(command)
            os.chdir('..')
            files = ''
            ijob+=1
        

jobscript = '''#!/bin/zsh
echo "$QUEUE $JOB $HOST"
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc530
cd CWD
eval `scramv1 runtime -sh`
#cmsenv
cd $TMPDIR
pwd
mkdir TnP
cd TnP
pwd
cp -r CWD/python python_
ls python_                                                                                                          
cd python_                    
pwd
cd -  
python python_/ANALYZER inputFiles="INFILE"
rm -rf python_
mv *.root CWD/TagProbeTrees/
cd ../
pwd
rm -rf TnP
'''

main()
