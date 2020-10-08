from ROOT import *
from utils import *
from namelib import *
import sys
from random import shuffle
#print 'Histogram factory starting........'
gStyle.SetOptStat(0)
gStyle.SetFrameBorderMode(0)
gStyle.SetLegendBorderSize(0)
gStyle.SetLegendTextSize(0.026)
try:fname =sys.argv[1]
except:
    fname = 'TagProbeTrees/TagnProbe_DYJetsToLL_M-50_100HT.root'
    print 'files not specified, will run on 4 default files:'
    print 'catau: 55 cm'

try:foname =sys.argv[2]
except:
    foname = 'Kappa.root'
    print 'Output file not specified, will create output as: Kappa.root'
f  = TFile(fname)
keys = f.GetListOfKeys()
#oname = [fname.rfind('/')+1:].replace('.root','')
#print oname
c1 = mkcanvas('c1')
'''
namelist = []

for key in keys:                                                                                                                                         
    name = key.GetName()
    print name              
    namelist.append(name[1:]) 
    

print 'namelib= {}' 
                                                                                                                                           
for name in namelist:                                                                                                                      
#    name = key.GetName() 
    print 'namelib["' + name + '"] = "' + name +'"'                                                                                                           

exit(0) 
'''
#c1.SetLogy()
'''
for key in keys:
    name = key.GetName()

    if not ('eff' in name):continue

#    if not ('DTeff' in name):continue
    print name
    hpass   = f.Get(name)
    print hpass.GetBinContent(1), 10*'*'
    hAll    = f.Get(name.replace('RECOeff','').replace('DTeff','').replace('eff',''))
#    hAll    = f.Get(name.replace('DTeff','RECOeff'))
#    continue
    histoStyler(hpass,kGreen+1)
    hpass.GetXaxis().SetTitle(name.replace('DTeff','').replace('RECOeff','').replace('MuProbe','').replace('h',''))
    leg = TLegend(0.17,0.67,0.51,0.89)
    leg.SetHeader("MC sample")
    hpass.GetYaxis().SetTitle('efficiency #epsilon')
    hpass.GetYaxis().SetRangeUser(0,1.15)
    stamp(1)
    print "hpass", hpass
    eff =TEfficiency(hpass,hAll)
    eff.SetLineWidth(1)
    eff.SetLineStyle(2)
    eff.SetMarkerStyle(22)
    eff.SetMarkerColor(1)

    leg.AddEntry(eff," DYtoLL  ","lep")

    hpass.SetTitle(namelib[name[1:]])
    hpass.Reset()
    hpass.Draw()
    
    eff.Draw('same')   #cool trick        


    leg.SetFillStyle(0)
#    leg.Draw()
    c1.Update()

    pause()
    c1.Print('pdf/eff'+name+'.pdf')
'''
fnew = TFile(foname,'recreate')
fnew.cd()
for key in keys:
    name = key.GetName()
    print name
    print 10*'*'
#    if not ('LDTeff' in name):continue 
    if not ('EtaDTeff' in name or 'PtDTeff' in name or 'ChargeDTeff' in name or 'PlusDTeff' in name or 'MinusDTeff' in name):continue

    hnum   = f.Get(name)
#    sf = hnum.GetRandom()
#    print sf, 10*'***''

    hden    = f.Get(name.replace('DTeff','RECOeff').replace('SCharge','Charge').replace('MCharge','Charge').replace('LCharge','Charge'))
    hden.GetXaxis().SetTitle(namelib[name.replace('DTeff','').replace('DTmeff','').replace('RECOeff','').replace('EleProbe','').replace('h','').replace('EleGen','')])
    leg2 = TLegend(0.17,0.67,0.51,0.89)
    leg2.SetHeader("MC sample")
    hden.GetYaxis().SetTitle('#kappa')
    hden.GetYaxis().SetRangeUser(0,0.008)
#    stamp(1)
    print "hnum 11", hnum.GetBinContent(1,4)
    print "hnum 00", hnum.GetBinContent(0,0)
    hnum.Divide(hden)
    print "hnum", hnum.GetBinContent(2)
    print 10*'*'
    leg2.AddEntry(hden," DYtoLL  ","lep")
    hden.SetTitle('#kappa from ' + name.replace('DTeff','').replace('DTmeff','').replace('RECOeff','').replace('EleProbe','Tag and Probe').replace('h','').replace('EleGen','Gen Info').replace('Pt','').replace('Eta',''))
#    hden.SetTitle(namelib[name[1:]])
    hden.Reset()
#    hden.Draw()

    hnum.Draw('same')   #cool trick                                                                                                                             


    leg2.SetFillStyle(0)
#    leg2.Draw()                                                                                                                                                
    c1.Update()

    pause()
    c1.Print('pdfef/Akappa'+name.replace('DTeff','').replace('DTmeff','').replace('RECOeff','').replace('EleProbe','Tag and Probe').replace('h','').replace('EleGen','Gen Info')+'.pdf')
    hnum.Write('Akappa'+name.replace('DTeff','').replace('DTmeff','').replace('RECOeff','').replace('EleProbe','tagNprobe').replace('h','').replace('EleGen','GenInfo'))
    print 'root file updated with histo'
fnew.Close()
print "file:", fnew, "created."
