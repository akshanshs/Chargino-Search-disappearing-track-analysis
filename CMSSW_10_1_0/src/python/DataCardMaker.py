import os , sys
from ROOT import *
from glob import glob
import scipy.constants as scc
from utilitiesII import *
import fileinput
import datetime


lumi = 35.9

try: HistFile = sys.argv[1]
except: HistFile = 'Limit_BinNumberAllBkg_Signal100.root'

try: DataCardTemplate = sys.argv[1]
except: DataCardTemplate = 'DC_template.txt'



today = datetime.date.today()

print 'plank', scc.physical_constants["Planck constant over 2 pi in eV s"][0]
print scc.c

######10cm

#masses = ['g1000_chi400', 'g1000_chi550', 'g1000_chi750', 'g1100_chi950', 'g1200_chi1050', 'g1200_chi550', 'g1200_chi750', 'g1200_chi950', 'g1300_chi1150', 'g1400_chi1050', 'g1400_chi1150', 'g1400_chi400', 'g1400_chi550', 'g1400_chi750', 'g1400_chi950', 'g1500_chi1150', 'g1500_chi1350', 'g1600_chi1050', 'g1600_chi1150', 'g1600_chi1350', 'g1600_chi400', 'g1600_chi550', 'g1600_chi750', 'g1600_chi950', 'g1700_chi1150', 'g1700_chi1350', 'g1700_chi1550', 'g1700_chi750', 'g1800_chi1050', 'g1800_chi1150', 'g1800_chi1350', 'g1800_chi400', 'g1800_chi550', 'g1800_chi750', 'g1800_chi950', 'g1900_chi1550', 'g1900_chi1750', 'g1900_chi750', 'g1900_chi950', 'g2000_chi1050', 'g2000_chi1150', 'g2000_chi1350', 'g2000_chi400', 'g2000_chi550', 'g2000_chi750', 'g2000_chi950', 'g2100_chi1550', 'g2100_chi1750', 'g2100_chi400', 'g2100_chi550', 'g2100_chi750', 'g2100_chi950', 'g2200_chi1050', 'g2200_chi1150', 'g2200_chi1350', 'g2200_chi1550', 'g2200_chi750', 'g2200_chi950', 'g2400_chi1050', 'g2400_chi1150', 'g2400_chi1350', 'g2400_chi1550', 'g2400_chi1750', 'g2400_chi400', 'g2400_chi550', 'g2400_chi750', 'g2400_chi950', 'g800_chi400', 'g800_chi550', 'g900_chi750','g1600_chi200', 'g1800_chi200', 'g2000_chi200', 'g2100_chi200', 'g2400_chi200', 'g800_chi200']

######30cm

masses = ['g1000_chi400', 'g1000_chi550', 'g1000_chi750', 'g1100_chi950', 'g1200_chi1050', 'g1200_chi750', 'g1200_chi950', 'g1300_chi1150', 'g1400_chi1050', 'g1400_chi1150', 'g1400_chi400', 'g1400_chi550', 'g1400_chi950', 'g1500_chi1350', 'g1600_chi1050', 'g1600_chi1150', 'g1600_chi1350', 'g1600_chi400', 'g1600_chi550', 'g1600_chi750', 'g1600_chi950', 'g1700_chi1150', 'g1700_chi1350', 'g1700_chi1550', 'g1700_chi750', 'g1800_chi1050', 'g1800_chi1150', 'g1800_chi1350', 'g1800_chi400', 'g1800_chi550', 'g1800_chi750', 'g1800_chi950', 'g1900_chi1150', 'g1900_chi1350', 'g1900_chi1550', 'g1900_chi1750', 'g1900_chi550', 'g1900_chi750', 'g1900_chi950', 'g2000_chi1050', 'g2000_chi1150', 'g2000_chi1350', 'g2000_chi400', 'g2000_chi550', 'g2000_chi750', 'g2000_chi950', 'g2100_chi1550', 'g2100_chi1750', 'g2100_chi400', 'g2100_chi550', 'g2100_chi750', 'g2100_chi950', 'g2200_chi1050', 'g2200_chi1150', 'g2200_chi1350', 'g2200_chi1550', 'g2200_chi550', 'g2200_chi750', 'g2200_chi950', 'g2300_chi1750', 'g2400_chi1050', 'g2400_chi1150', 'g2400_chi1350', 'g2400_chi1550', 'g2400_chi1750', 'g2400_chi400', 'g2400_chi550', 'g2400_chi750', 'g2400_chi950', 'g800_chi400', 'g800_chi550', 'g900_chi750','g1600_chi200', 'g1800_chi200', 'g2000_chi200', 'g2100_chi200', 'g2400_chi200', 'g800_chi200']

######50cm

#masses = ['g1000_chi550', 'g1000_chi750', 'g1100_chi950', 'g1200_chi550', 'g1200_chi750', 'g1200_chi950', 'g1300_chi1150', 'g1400_chi1050', 'g1400_chi1150', 'g1400_chi550', 'g1400_chi750', 'g1400_chi950', 'g1500_chi1350', 'g1600_chi1200', 'g1600_chi1350', 'g1600_chi550', 'g1600_chi750', 'g1600_chi950', 'g1700_chi1300', 'g1700_chi1350', 'g1700_chi1450', 'g1700_chi1550', 'g1800_chi1150', 'g1800_chi1350', 'g1800_chi550', 'g1800_chi750', 'g1800_chi950', 'g1850_chi1450', 'g1900_chi1750', 'g2000_chi1000', 'g2000_chi1150', 'g2000_chi1200', 'g2000_chi1350', 'g2000_chi1450', 'g2000_chi550', 'g2000_chi750', 'g2000_chi950', 'g2100_chi1150', 'g2100_chi1350', 'g2100_chi1450', 'g2100_chi1550', 'g2100_chi1750', 'g2100_chi550', 'g2100_chi700', 'g2100_chi750', 'g2100_chi950', 'g2200_chi1150', 'g2200_chi1350', 'g2200_chi1550', 'g2200_chi550', 'g2200_chi750', 'g2200_chi950', 'g2300_chi1150', 'g2300_chi1350', 'g2300_chi1550', 'g2300_chi1750', 'g2300_chi550', 'g2300_chi750', 'g2300_chi950', 'g2400_chi1150', 'g2400_chi1350', 'g2400_chi1550', 'g2400_chi1750', 'g2400_chi550', 'g2400_chi750', 'g2400_chi950', 'g700_chi550', 'g800_chi550', 'g900_chi750','g1800_chi1400', 'g1800_chi1500', 'g1900_chi1000', 'g1900_chi1400', 'g1900_chi1600', 'g2000_chi1600', 'g2400_chi1300', 'g2400_chi1700', 'g1000_chi400', 'g1400_chi400', 'g1600_chi200', 'g1600_chi400', 'g1800_chi200', 'g1800_chi400', 'g2000_chi200', 'g2000_chi400', 'g2100_chi200', 'g2100_chi400', 'g2400_chi200', 'g2400_chi400', 'g700_chi200', 'g700_chi400', 'g800_chi200', 'g800_chi400']


lifetimes = ['10','30','50','100']
suffixes = [['',''],['_up','_SysUp'],['_down','_SysDown']]


def makeonedatacard( mass = 'g2400_chi1300', lifetime = '30'):

  filename = 'Limit_BinNumberAllBkg_Signal'+mass+'_'+lifetime+'cm.root'
  histlist = ['Signal'+mass,'Electron','Muon','Tau','Fake','data_obs']
  
  HistFile = TFile(filename)

  with open(DataCardTemplate,'r') as f:
    lines = f.readlines()
    print lines

    DC_file = 'datacard_'+mass+'LT'+lifetime+'cm.txt'
    with open(DC_file,'w') as fw:

      for iline,line in enumerate(lines):
        print line
        if 'zzz'  in line: line = line.replace('zzz',str(lumi))
        if 'XXX'  in line: line = line.replace('XXX',str(today))
        if 'HHHH' in line: line = line.replace('HHHH',filename)
        if 'YYY'  in line: line = line.replace('YYY',mass)
        if 'SSS'  in line: line = line.replace('SSS',str((HistFile.Get(histlist[0])).Integral()))
        if 'EEE'  in line: line = line.replace('EEE',str((HistFile.Get(histlist[1])).Integral()))
        if 'MMM'  in line: line = line.replace('MMM',str((HistFile.Get(histlist[2])).Integral()))
        if 'TTT'  in line: line = line.replace('TTT',str((HistFile.Get(histlist[3])).Integral()))
        if 'FFF'  in line: line = line.replace('FFF',str((HistFile.Get(histlist[4])).Integral()))
        if 'OOO'  in line: line = line.replace('OOO',str((HistFile.Get(histlist[5])).Integral()))
        fw.write(line)
        print line
        #pause()
      print 'created a data card for '+mass+'50 cm signal: ', fw.name
def main():


  for imass, mass in enumerate(masses):
  
#  makeonedatacard( mass = 'g2400_chi1300', lifetime = '50')
#  makeonedatacard( mass = 'g2400_chi1700', lifetime = '50')
#  makeonedatacard( mass = 'g2500_chi1700', lifetime = '50')
#  makeonedatacard( mass = 'g2600_chi1700', lifetime = '50')
    makeonedatacard( mass = mass, lifetime = '30')
main()
