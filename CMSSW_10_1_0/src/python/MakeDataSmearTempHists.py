from ROOT import *
from utilities import *
from histlib import *
from titlelib import *
import sys

#gROOT.SetBatch(1)

gStyle.SetOptStat(0)
gStyle.SetFrameBorderMode(0)
gStyle.SetLegendBorderSize(0)
gStyle.SetLegendTextSize(0.026)

##################################################################
#scripts takes in two files, and the name of two histo grams to be compared
#If the hists in same fie has to be compared: input the second file same as first
#################################################################



try:fname =sys.argv[1]
except:
    fname = 'TagProbeTrees/TagnProbeHists_Run2016noSmearDM10.root'
print 'file I : ', fname

try:KEYI = sys.argv[2]
except:
    KEYI = 'htrkresp'

f  = TFile(fname)

keys = f.GetListOfKeys()

histlist = []
c1 = mkcanvas(KEYI)
fnew = TFile('Response_Data.root','recreate')
fnew.cd()

for key in keys:
    c1.SetLogy()
    hist = key.GetName()
    print hist
    if ('vs' in hist):continue 
#    if '(1.566, 2.4)' in hist: continue
    if not ('El' in hist): continue
    print hist , 'this passed eta requirements'
    if not (KEYI in hist):continue # 
    histlist.append(hist[1:])
    h     =  f.Get(hist)
    h2    =  f.Get(hist.replace('El','Mu'))
    overflow(h)
    overflow(h2)
######Normlise Hists
    n = 1
    h_entries = h.Integral(-9999,9999)#h.GetEntries()
    print 'Integral', h.Integral(-9999,9999), 'Get Entries :', h.GetEntries() 
    if not (h_entries) > 0:h_entries = 1
    s1= n/h_entries
    h.Scale(s1)
    h2_entries = h2.Integral(-9999,9999) #h2.GetEntries()
    if not (h2_entries) > 0:h2_entries = 1
    s2= n/h2_entries
    h2.Scale(s2)
    pdfname = hist[1:].replace('((1.566, 2.4),', ' EndCap Pt').replace('((0, 1.4442), ', ' Barrel Pt').replace('))',')')
    print pdfname
    pause()
    legHeader = hist[1:].replace('((1.566, 2.4),', ' EndCap P_{T}').replace('((0, 1.4442), ', ' Barrel P_{T}').replace('trkresp','').replace('))',') GeV').replace(', ',' - ').replace('El','').replace('Mu','')
    print legHeader
    leg = mklegend(x1=.54, y1=.72, x2= 0.91, y2=.91, color=kWhite)
    
    leg.SetHeader('  '+legHeader)#MC:DYtoLNuLNu")
    leg.SetTextSize(0.045)
    histoStyler(h,4)
    h.SetLineWidth(2)
    h.SetLineStyle(1)

    histoStyler(h2,2)
    h2.SetLineWidth(2)
    h2.SetLineStyle(1)
    
    TGaxis.SetMaxDigits(2)

    leg.AddEntry(h,'Disappearing track (e)',"l") #Tag + l_{(probe)}                                                                                                 
#    leg.AddEntry(h2,'Disappearing track'+' (\mu)',"l")
    c1.Update()
    c1.cd(1)
    print 'going to draw', hist, 'header name', legHeader
    pause()
    h.Draw('hist e1')
#    TGaxis.SetMaxDigits(2)
    h.GetYaxis().SetTitleOffset(1.08)
    h.GetYaxis().SetTitleSize(.055)
    h.GetXaxis().SetTitleOffset(1)
    h.GetXaxis().SetNoExponent(kTRUE)
#    h.GetYaxis().SetNoExponent(kTRUE)
    h.GetXaxis().SetTitleSize(.055)
    h.GetXaxis().SetTitle('Response')#Invariant Mass (ll)')#histlib[hist[1:]])
    h.GetYaxis().SetRangeUser(0.0001,15*(max(h.GetMaximum(),h2.GetMaximum())))
    h.GetYaxis().SetTitle('Events normalized to unity')
    h.SetTitle('')
#    h.SetTitle(titlelib[hist[1:]])

    h.Draw('hist e1')
#    h2.Draw('histsame e1')
#    leg.SetFillStyle(0)
    leg.Draw()
    stamp()
    c1.Update()
    fnew.cd()
    c1.Write(legHeader.replace(' ','_'))
    pause()
    c1.Print('compHist_pdf/'+pdfname.replace(' ','_')+'.png')
    print 'created:' ,'compHist_pdf/'+pdfname.replace(' ','_')+'.png'
print 'just made', fnew.GetName()
fnew.Close()
exit(0)
