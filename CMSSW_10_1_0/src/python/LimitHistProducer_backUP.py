import os , sys
from ROOT import *
from glob import glob
import scipy.constants as scc
from utilitiesII import *

try: fnameSig10 = sys.argv[1]
except: yo = 1 #fnameSig10 = 'g1800_chi1400_27_200970_step4_10AODScaledtest.root'
#Sigfilename = TFile(fnameSig10)


try: prompt_file = sys.argv[2]          # same file for El and Mu                                                
except: prompt_file = 'Prompt_test.root'
print prompt_file
El = TFile(prompt_file)

try: prompt_file = sys.argv[2]          # same file for El and Mu                                             
except: prompt_file = 'Prompt_test.root'
print prompt_file
Mu = TFile(prompt_file)

try: fake_file = sys.argv[3]
except: fake_file = 'Fake_test.root'
print fake_file
Fake = TFile(fake_file)

try: tau_file = sys.argv[4]
except: tau_file = 'Tau_test.root'
print tau_file
Tau = TFile(tau_file)

try: data_file = sys.argv[5]
except: data_file = 'Data_test.root'
print data_file
Data = TFile(data_file)

print 'plank', scc.physical_constants["Planck constant over 2 pi in eV s"][0]
print scc.c
lifetimes = ['10','30','50','100']
suffixes = [['',''],['_up','_SysUp'],['_down','_SysDown']]
keys = Data.GetListOfKeys()
def main():

  for isig, SigSuffix in enumerate(lifetimes):
    fnameSig = 'g1800_chi1400_27_200970_step4_'+SigSuffix+'AODScaledtest.root'
    Sigfilename = TFile(fnameSig)


    filenames = [[Sigfilename,'Signal' ,'Signal'+SigSuffix],[El,'El','Electron'],[Mu,'Mu','Muon'],[Fake,'Fake','Fake'],[Tau,'Tau','Tau'],[Data,'Data','data_obs']]    # [filename, oldhistname, newhistname]

    histkey = 'SignalRegion1jet_BinNumberMethod'
    print 'histkey: ', histkey

    fnew = TFile('Limit_BinNumber'+'AllBkg_'+'Signal'+SigSuffix+'.root','recreate')
    fnew.cd()
    for ifilename, filename in enumerate(filenames):
      for isuffix, suffix in enumerate(suffixes):
        histname      = 'h'+filename[1]+histkey+suffix[0]
        newhistname = filename[2]+suffix[1]
        print 'histname: ' ,histname
        print 'newhistname: ', newhistname
        hist = filename[0].Get(histname)
        hist.SetName(newhistname)
        hist.Write()
    fnew.Close()
    print "Just created", fnew

main()
