from ROOT import *
from utils import *
from namelib import *
import sys 

print 'Histogram factory starting........'
gStyle.SetOptStat(0)
gStyle.SetFrameBorderMode(0)
gStyle.SetLegendBorderSize(0)
gStyle.SetLegendTextSize(0.026)
try:fname =sys.argv[1]
except:
    fname = 'output55.root'
    print 'files not specified, will run on 4 default files:'
    print 'catau: 55 cm'
try:fname2 = sys.argv[2]
except:
    fname2 = 'output90.root'
    print 'catau: 90 cm'
try:fname3 = sys.argv[3]
except:
    fname3 = 'output10.root'
    print 'catau: 10 cm'
try:fname4 = sys.argv[4]
except:
    fname4 = 'output22.root'
    print 'catau: 22 cm'

f  = TFile(fname)
f2 = TFile(fname2)
f3 = TFile(fname3)
f4 = TFile(fname4)
keys = f.GetListOfKeys()

c1 = mkcanvas('c1')

namelist = []

###########Olny for 2D Hists
'''
c1.SetLogz()
for key in keys:
    name = key.GetName()

    if not ('vs' in name):continue
    yname,xname = name[1:].split('vs')
    h    = f.Get(name)
    namelist.append(xname)
    namelist.append(yname)
    histoStyler(h,kRed+1)
    h.GetXaxis().SetTitle(namelib[xname])
    h.GetYaxis().SetTitle(namelib[yname])
    h.Draw('colz')
#    h2    = f2.Get(name)                                                                                                                                            
#    histoStyler(h2,kBlue+1)                                                                                                                                         
#    h2.Draw('same')                                                                                                                                                 
    c1.Update()

    pause()
    c1.Print('pdf/'+name+'.pdf')
'''







############






'''
for key in keys:
    name = key.GetName()
    print name
    namelist.append(name[1:])
    c1.Update()


print 'namelib= {}'
for name in namelist:
    name = key.GetName()
    print 'namelib["' + name + '"] = "' + name +'"'

exit(0)
'''

for key in keys:
    name = key.GetName()
    print name
    if not ('Tag' in name):continue
    hpass    = f.Get(name)
    hAll    = f.Get(name.replace('Tag',''))

    histoStyler(hpass,kGreen+1)
    hpass.GetXaxis().SetTitle(namelib[name[1:].replace('Tag','')])

#    hpass.Divide(hAll)

    leg = TLegend(0.17,0.67,0.51,0.89)
    leg.SetHeader("Signal point (ctau,mass)")
    hpass.GetYaxis().SetTitle('efficiency #epsilon')
    hpass.GetYaxis().SetRangeUser(0,1.25)
    stamp(1)
    hpass2    = f2.Get(name)
    hAll2    = f2.Get(name.replace('Tag',''))
    hpass3    = f3.Get(name)
    hAll3    = f3.Get(name.replace('Tag',''))
    hpass4    = f4.Get(name)
    hAll4    = f4.Get(name.replace('Tag',''))

    eff2 =TEfficiency(hpass2,hAll2)
    eff3 =TEfficiency(hpass3,hAll3)
    eff4 =TEfficiency(hpass4,hAll4)

    eff3.SetLineWidth(1)
    eff3.SetLineStyle(2)
    eff3.SetMarkerStyle(20)
    eff3.SetMarkerColor(3)

    eff4.SetLineWidth(1)
    eff4.SetLineStyle(2)
    eff4.SetMarkerStyle(23)
    eff4.SetMarkerColor(4)

    eff =TEfficiency(hpass,hAll)
    eff.SetLineWidth(1)
    eff.SetLineStyle(2)
    eff.SetMarkerStyle(22)
    eff.SetMarkerColor(1)
    eff2.SetLineWidth(1)
    eff2.SetLineStyle(10)
    eff2.SetMarkerStyle(33)
    eff2.SetMarkerColor(2)

    leg.AddEntry(eff,"55 cm ,1100 GeV ","lep")
    leg.AddEntry(eff2,"90 cm,500 GeV","lep")
    leg.AddEntry(eff3,"10  cm,1200 GeV","lep")
    leg.AddEntry(eff4,"22 cm,900 GeV","lep")
    hpass.SetTitle("Detecting disappearing tracks from gen information")
    hpass.Reset()
    hpass.Draw()
    eff.Draw('same')   #cool trick
    eff2.Draw('same')
    eff3.Draw('same')
    eff4.Draw('same')
    leg.SetFillStyle(0)
    leg.Draw()
    c1.Update()

    pause()
    c1.Print('pdf/eff'+name+'.pdf')
'''
#c1.SetLogy()
for key in keys:
    c1.SetLogy()
    name = key.GetName()
    print name
    if 'vs' in name:continue
    namelist.append(name[1:])
    h    = f.Get(name)
    h2    = f2.Get(name)
    h3    = f3.Get(name)
    h4    = f4.Get(name)
    overflow(h)
    overflow(h2)
    overflow(h3)
    overflow(h4)
    n = 1
#    s1= n/(h.Integral())
#    h.Scale(s1)
#    s2= n/(h2.Integral())
#    h2.Scale(s2)
#    s3= n/(h3.Integral())
#    h3.Scale(s3)
#    s4= n/(h4.Integral())
#    h4.Scale(s4)


    leg = TLegend(0.66,0.67,0.87,0.89)
    leg.SetHeader("Signal point (ctau,mass)")
    histoStyler(h,1)
    h.SetLineWidth(2)
    h.SetLineStyle(2)
    h.GetXaxis().SetTitle(namelib[name[1:]])
    h.GetYaxis().SetRangeUser(0.1,5*max(h.GetMaximum(),h2.GetMaximum()))
    if 'pfMET' or 'nDT' in name:h.GetYaxis().SetTitle('number of events') #chi^{#pm}')
    if 'pfMET' or 'nDT' not in name:h.GetYaxis().SetTitle('number of events') #chi^{#pm}')
    h.Draw('hist')
    histoStyler(h2,2)
    histoStyler(h3,3)
    histoStyler(h4,4)
    h2.SetLineWidth(2)
    h2.SetLineStyle(2)
    h3.SetLineWidth(2)
    h3.SetLineStyle(2)
    h4.SetLineWidth(2)
    h4.SetLineStyle(2)
    leg.AddEntry(h,"55 cm ,1100 GeV ","l")
    leg.AddEntry(h2,"90 cm,500 GeV","l")
    leg.AddEntry(h3,"10 cm ,1200 GeV ","l")
    leg.AddEntry(h4,"22 cm,900 GeV","l")
#    h2.Draw('hist')
    h2.Draw('histsame')
    h3.Draw('histsame')
    h4.Draw('histsame')
    leg.SetFillStyle(0)
    leg.Draw()
    c1.Update()
    
    pause()
    c1.Print('pdf/'+name+'.pdf')
'''
for key in keys:
    name = key.GetName()
    print name
    if not ('Tag' in name):continue
    hpass    = f.Get(name)
    hAll    = f.Get(name.replace('Tag',''))

    histoStyler(hpass,kGreen+1)
    hpass.GetXaxis().SetTitle(namelib[name[1:].replace('Tag','')])

#    hpass.Divide(hAll)                                                                                                                                                                                                                                                        

    leg = TLegend(0.17,0.67,0.51,0.89)
    leg.SetHeader("Signal point (ctau,mass)")
    hpass.GetYaxis().SetTitle('efficiency #epsilon')
    hpass.GetYaxis().SetRangeUser(0,1.1)
    stamp(1)
    hpass2    = f2.Get(name)
    hAll2    = f2.Get(name.replace('Tag',''))
    hpass3    = f3.Get(name)
    hAll3    = f3.Get(name.replace('Tag',''))
    hpass4    = f4.Get(name)
    hAll4    = f4.Get(name.replace('Tag',''))

    eff2 =TEfficiency(hpass2,hAll2)
    eff3 =TEfficiency(hpass3,hAll3)
    eff4 =TEfficiency(hpass4,hAll4)

    eff3.SetLineWidth(1)
    eff3.SetLineStyle(2)
    eff3.SetMarkerStyle(20)
    eff3.SetMarkerColor(3)

    eff4.SetLineWidth(1)
    eff4.SetLineStyle(2)
    eff4.SetMarkerStyle(23)
    eff4.SetMarkerColor(4)

    eff =TEfficiency(hpass,hAll)
    eff.SetLineWidth(1)
    eff.SetLineStyle(2)
    eff.SetMarkerStyle(22)
    eff.SetMarkerColor(1)
    eff2.SetLineWidth(1)
    eff2.SetLineStyle(10)
    eff2.SetMarkerStyle(33)
    eff2.SetMarkerColor(2)

    leg.AddEntry(eff,"55 cm ,1100 GeV ","lep")
    leg.AddEntry(eff2,"90 cm,500 GeV","lep")
    leg.AddEntry(eff3,"3  cm,700 GeV","lep")
    leg.AddEntry(eff4,"22 cm,900 GeV","lep")
    hpass.SetTitle("Detecting disappearing tracks from gen information")
    hpass.Reset()
    hpass.Draw()
    eff.Draw('same')   #cool trick                                                                                                                                                                                                                                             
    eff2.Draw('same')
    eff3.Draw('same')
    eff4.Draw('same')
    leg.Draw()
    c1.Update()

    pause()
    c1.Print('pdf/eff'+name+'.pdf')
'''
c1.SetLogz()    
for key in keys:
    name = key.GetName()
    
    if not ('vs' in name):continue
    yname,xname = name[1:].split('vs')
    h    = f.Get(name)
    namelist.append(xname)
    namelist.append(yname)
    histoStyler(h,kRed+1)
    h.GetXaxis().SetTitle(namelib[xname])
    h.GetYaxis().SetTitle(namelib[yname])
    h.Draw('colz')
#    h2    = f2.Get(name)
#    histoStyler(h2,kBlue+1)
#    h2.Draw('same')
    c1.Update()

    pause()
    c1.Print('pdf/'+name+'.pdf')

print 'namelib= {}'
for name in namelist:
    print 'namelib["' + name + '"] = "' + name +'"'

