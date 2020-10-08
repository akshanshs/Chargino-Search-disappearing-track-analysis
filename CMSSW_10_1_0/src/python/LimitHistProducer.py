import os , sys
from ROOT import *
from glob import glob
import scipy.constants as scc
from utilitiesII import *

try: fnameSig10 = sys.argv[1]
except: yo = 1 #fnameSig10 = 'g1800_chi1400_27_200970_step4_10AODScaledtest.root'
#Sigfilename = TFile(fnameSig10)


try: prompt_file = sys.argv[2]          # same file for El and Mu                                                
except: prompt_file = 'Prompt_test2.root'
print prompt_file
El = TFile(prompt_file)

try: prompt_file = sys.argv[2]          # same file for El and Mu                                             
except: prompt_file = 'Prompt_test2.root'
print prompt_file
Mu = TFile(prompt_file)

try: fake_file = sys.argv[3]
except: fake_file = 'Fake_test2.root'
print fake_file
Fake = TFile(fake_file)

try: tau_file = sys.argv[4]
except: tau_file = 'Tau_test2.root'
print tau_file
Tau = TFile(tau_file)

try: data_file = sys.argv[5]
except: data_file = 'Data_test.root'
print data_file
Data = TFile(data_file)

print 'plank', scc.physical_constants["Planck constant over 2 pi in eV s"][0]
print scc.c


################10cm#############

masses = ['g1000_chi400', 'g1000_chi550', 'g1000_chi750', 'g1100_chi950', 'g1200_chi1050', 'g1200_chi550', 'g1200_chi750', 'g1200_chi950', 'g1300_chi1150', 'g1400_chi1050', 'g1400_chi1150', 'g1400_chi400', 'g1400_chi550', 'g1400_chi750', 'g1400_chi950', 'g1500_chi1150', 'g1500_chi1350', 'g1600_chi1050', 'g1600_chi1150', 'g1600_chi1350', 'g1600_chi400', 'g1600_chi550', 'g1600_chi750', 'g1600_chi950', 'g1700_chi1150', 'g1700_chi1350', 'g1700_chi1550', 'g1700_chi750', 'g1800_chi1050', 'g1800_chi1150', 'g1800_chi1350', 'g1800_chi400', 'g1800_chi550', 'g1800_chi750', 'g1800_chi950', 'g1900_chi1550', 'g1900_chi1750', 'g1900_chi750', 'g1900_chi950', 'g2000_chi1050', 'g2000_chi1150', 'g2000_chi1350', 'g2000_chi400', 'g2000_chi550', 'g2000_chi750', 'g2000_chi950', 'g2100_chi1550', 'g2100_chi1750', 'g2100_chi400', 'g2100_chi550', 'g2100_chi750', 'g2100_chi950', 'g2200_chi1050', 'g2200_chi1150', 'g2200_chi1350', 'g2200_chi1550', 'g2200_chi750', 'g2200_chi950', 'g2400_chi1050', 'g2400_chi1150', 'g2400_chi1350', 'g2400_chi1550', 'g2400_chi1750', 'g2400_chi400', 'g2400_chi550', 'g2400_chi750', 'g2400_chi950', 'g800_chi400', 'g800_chi550', 'g900_chi750']

#################30cm#############
#masses = ['g1000_chi400', 'g1000_chi550', 'g1000_chi750', 'g1100_chi950', 'g1200_chi1050', 'g1200_chi750', 'g1200_chi950', 'g1300_chi1150', 'g1400_chi1050', 'g1400_chi1150', 'g1400_chi400', 'g1400_chi550', 'g1400_chi950', 'g1500_chi1350', 'g1600_chi1050', 'g1600_chi1150', 'g1600_chi1350', 'g1600_chi400', 'g1600_chi550', 'g1600_chi750', 'g1600_chi950', 'g1700_chi1150', 'g1700_chi1350', 'g1700_chi1550', 'g1700_chi750', 'g1800_chi1050', 'g1800_chi1150', 'g1800_chi1350', 'g1800_chi400', 'g1800_chi550', 'g1800_chi750', 'g1800_chi950', 'g1900_chi1150', 'g1900_chi1350', 'g1900_chi1550', 'g1900_chi1750', 'g1900_chi550', 'g1900_chi750', 'g1900_chi950', 'g2000_chi1050', 'g2000_chi1150', 'g2000_chi1350', 'g2000_chi400', 'g2000_chi550', 'g2000_chi750', 'g2000_chi950', 'g2100_chi1550', 'g2100_chi1750', 'g2100_chi400', 'g2100_chi550', 'g2100_chi750', 'g2100_chi950', 'g2200_chi1050', 'g2200_chi1150', 'g2200_chi1350', 'g2200_chi1550', 'g2200_chi550', 'g2200_chi750', 'g2200_chi950', 'g2300_chi1750', 'g2400_chi1050', 'g2400_chi1150', 'g2400_chi1350', 'g2400_chi1550', 'g2400_chi1750', 'g2400_chi400', 'g2400_chi550', 'g2400_chi750', 'g2400_chi950', 'g800_chi400', 'g800_chi550', 'g900_chi750']
#################50cm#############

#masses = ['g1000_chi550', 'g1000_chi750', 'g1100_chi950', 'g1200_chi550', 'g1200_chi750', 'g1200_chi950', 'g1300_chi1150', 'g1400_chi1050', 'g1400_chi1150', 'g1400_chi550', 'g1400_chi750', 'g1400_chi950', 'g1500_chi1350', 'g1600_chi1200', 'g1600_chi1350', 'g1600_chi550', 'g1600_chi750', 'g1600_chi950', 'g1700_chi1300', 'g1700_chi1350', 'g1700_chi1450', 'g1700_chi1550', 'g1800_chi1150', 'g1800_chi1350', 'g1800_chi550', 'g1800_chi750', 'g1800_chi950', 'g1850_chi1450', 'g1900_chi1750', 'g2000_chi1000', 'g2000_chi1150', 'g2000_chi1200', 'g2000_chi1350', 'g2000_chi1450', 'g2000_chi550', 'g2000_chi750', 'g2000_chi950', 'g2100_chi1150', 'g2100_chi1350', 'g2100_chi1450', 'g2100_chi1550', 'g2100_chi1750', 'g2100_chi550', 'g2100_chi700', 'g2100_chi750', 'g2100_chi950', 'g2200_chi1150', 'g2200_chi1350', 'g2200_chi1550', 'g2200_chi550', 'g2200_chi750', 'g2200_chi950', 'g2300_chi1150', 'g2300_chi1350', 'g2300_chi1550', 'g2300_chi1750', 'g2300_chi550', 'g2300_chi750', 'g2300_chi950', 'g2400_chi1150', 'g2400_chi1350', 'g2400_chi1550', 'g2400_chi1750', 'g2400_chi550', 'g2400_chi750', 'g2400_chi950', 'g700_chi550', 'g800_chi550', 'g900_chi750','g1800_chi1400', 'g1800_chi1500', 'g1900_chi1000', 'g1900_chi1400', 'g1900_chi1600', 'g2000_chi1600', 'g2400_chi1300', 'g2400_chi1700'] 


lifetimes = ['10','30','50','100']
suffixes = [['',''],['_up','_SysUp'],['_down','_SysDown']]
keys = Data.GetListOfKeys()
def main():

  for isig, SigSuffix in enumerate(masses):
    fnameSig = SigSuffix+'ScaledSignal.root'
#    fnameSig = 'g1800_chi1400_27_200970_step4_'+SigSuffix+'AODScaledtest.root'
    Sigfilename = TFile(fnameSig)


    filenames = [[Sigfilename,'Signal' ,'Signal'+SigSuffix],[El,'El','Electron'],[Mu,'Mu','Muon'],[Fake,'Fake','Fake'],[Tau,'Tau','Tau'],[Data,'Data','data_obs']]    # [filename, oldhistname, newhistname]


    histkey = 'SignalRegion1jet_BinNumberMethod'
    print 'histkey: ', histkey

    fnew = TFile('Limit_BinNumber'+'AllBkg_'+'Signal'+SigSuffix+'_'+lifetimes[0]+'cm.root','recreate')
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
