import os , sys
from ROOT import *
from glob import glob
import scipy.constants as scc

filelist = glob('*Hists*.root')

#print filelist                                                                                                                                                

print 'number of files:', len(filelist)

print 'plank', scc.physical_constants["Planck constant over 2 pi in eV s"][0]
print scc.c


def main():

  for ifname, filename in enumerate(filelist):

   #     if ifname%100 == 0:
      print ifname, filename
#      identifier = filename[filename.rfind('/')+1:].replace('.root','').replace('Summer16.','').replace('RA2AnalysisTree','')
#      fnew = TFile('bkgHistsSc_'+identifier+'.root','recreate')
      f = TFile(filename)
      keys = f.GetListOfKeys()
#      print identifier
#      print 'bkgHistsSc_'+identifier+'.root'
      n = 1
      for key in keys:
        hist = key.GetName()
        if ('hHTnum' in hist): 
          h = f.Get(hist)
#          n = h.Integral()
          n = h.Integral(-1,9999)
#          bin = h.GetNbinsX()+1
#          c = h.GetBinContent(bin)
#          n= n+c
#          print h.Integral()
      if n==0:
        print 'WARNING: tree with zero entries'
        continue
      identifier = filename[filename.rfind('/')+1:].replace('.root','').replace('Summer16.','').replace('RA2AnalysisTree','')
      fnew = TFile('bkgHistsSc_'+identifier+'.root','recreate')
      fnew.cd()
      for key2 in keys:
        hist2 = key2.GetName()
        if ('hHTnum' in hist2): continue
        h2 = f.Get(hist2)
        h2.Scale(1/n)
        h2.Write()
      print "Just created", fnew
      fnew.Close()
main()
