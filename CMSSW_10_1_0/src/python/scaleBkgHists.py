import os , sys
from ROOT import *
from glob import glob
import scipy.constants as scc
from utilitiesII import *

filelist = glob('CB_TagnProbeHists*.root')

lumi = 35900

print 'number of files:', len(filelist)

print 'plank', scc.physical_constants["Planck constant over 2 pi in eV s"][0]
print scc.c

def main():

  for ifname, filename in enumerate(filelist):
      print ifname, filename
      f = TFile(filename)
      keys = f.GetListOfKeys()
      n = 1
      n2 = 1 # from the method 'GetEntries()'
      for key in keys:
        hist = key.GetName()
        if ('hHtWeighted' in hist):continue
        if ('hHt' in hist): 
          h = f.Get(hist)
          n = h.Integral(-1,9999)
          n2 = h.GetEntries()
          print 'number of events from integration =', n
          print 'number of events from GetEntries() method =', n2
#          print 'number of events =', n
          pause()
      if n==0:
        print 'WARNING: tree with zero entries'
        continue
      identifier = filename[filename.rfind('/')+1:].replace('.root','').replace('Summer16.','').replace('RA2AnalysisTree','')
      fnew = TFile('Scaled_'+identifier+'.root','recreate')
      fnew.cd()
      pause()
      for key2 in keys:
        hist2 = key2.GetName()
        if ('hHt' in hist2):
          h2 = f.Get(hist2)
          h2.Write()
          continue
        h2 = f.Get(hist2)
        print n , 'will scale with this'
        h2.Scale(lumi/(n))
        h2.Write()
      print "Just created", fnew
      fnew.Close()
main()
