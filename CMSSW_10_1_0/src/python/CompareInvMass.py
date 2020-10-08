from ROOT import *
from utilities import *
from histlib import *
from titlelib import *
import sys

gROOT.SetBatch(1)

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

try:fname2 =sys.argv[1]
except:
    fname2 = 'TagProbeTrees/TagnProbeHists_Run2016noSmearDM10.root'
print 'file II : ', fname2

try:KEYI = sys.argv[2]
except:
    KEYI = 'DTnum'
print 'key I : ', KEYI

try:KEYII = sys.argv[3]
except:
    KEYII = 'RECOden'
print 'key II : ', KEYII

pause()
#histolib = {}
#histolib['iso'] = 'relIso'


f  = TFile(fname)
f2 = TFile(fname2)

keys = f.GetListOfKeys()
#f.ls()
#*=*=*=*=*=for makinghist from a flat tuple
#t1 = f1.Get('Analysis')

#t1.Show(0)

#for histkey in histolib:
#    t1.Draw(histolib[histkey])
#    t2.Draw(histolib[histkey],'same')
    
#    c1.Update()
#    #pause()

#c1 = mkcanvas2fig('c1')
histlist = []
c1 = mkcanvas(KEYI)
fnew = TFile('InvMass_comparions.root','recreate')
fnew.cd()

for key in keys:
#    c1.SetLogy()
    hist = key.GetName()
    print hist
    if ('vs' in hist):continue 
    if 'eta1.4442to1.566' in hist: continue
    if not ('hInvMass' in hist): continue
    if not (KEYI in hist):continue # 
    histlist.append(hist[1:])
    h     =  f.Get(hist)
    hist2 = hist.replace(KEYI,KEYII)
    h2    =  f2.Get(hist2)
    overflow(h)
    overflow(h2)
    
######Normlise Hists
    n = 1
    h_entries = h.GetEntries()
    if not (h_entries) > 0:h_entries = 1
    s1= n/h_entries
    h.Scale(s1)
    h2_entries = h2.GetEntries()
    if not (h2_entries) > 0:h2_entries = 1
    s2= n/h2_entries
    h2.Scale(s2)
    pdfname = hist[1:].replace('_eta1.566to2.4_', ' EndCap ').replace('_eta0to1.4442_', ' Barrel ').replace('_DTnum', '').replace('_RECOden', '')
    legHeader = hist[1:].replace('_eta1.566to2.4_', ' EndCap ').replace('_eta0to1.4442_', ' Barrel ').replace('_DTnum', '').replace('_RECOden', '').replace('Mu','').replace('El','').replace('pt','P_{T}(').replace('to',' - ').replace('InvMass','')+') GeV'
    leg = mklegend(x1=.54, y1=.72, x2= 0.91, y2=.91, color=kWhite)
    leg.SetHeader(legHeader)#MC:DYtoLNuLNu")
    leg.SetTextSize(0.045)
    histoStyler(h,2)
    h.SetLineWidth(2)
    h.SetLineStyle(1)

    histoStyler(h2,4)
    h2.SetLineWidth(2)
    h2.SetLineStyle(1)

    if 'El' in hist:
        leg.AddEntry(h,'IM (e_{tag} + e_{disp trk})',"l") #Tag + l_{(probe)}                                                                                                 
        leg.AddEntry(h2,'IM (e_{tag} + e_{reco})',"l")
    if 'Mu' in hist:
        leg.AddEntry(h,'IM (\mu_{tag} + \mu_{disp trk})',"l")
        leg.AddEntry(h2,'IM (\mu_{tag} + \mu_{reco})',"l")
    c1.Update()
    c1.cd(1)

    h.Draw('hist e1')
    TGaxis.SetMaxDigits(2)
    h.GetYaxis().SetTitleOffset(1.03)
    h.GetYaxis().SetTitleSize(.055)
    h.GetXaxis().SetTitleOffset(1)
    h.GetXaxis().SetNoExponent(kTRUE)
    h.GetXaxis().SetTitleSize(.055)
    h.GetXaxis().SetTitle('Invariant mass [GeV]')#Response')#Invariant Mass (ll)')#histlib[hist[1:]])
    h.GetYaxis().SetRangeUser(.0001,1.5*(max(h.GetMaximum(),h2.GetMaximum())))
    h.GetYaxis().SetTitle('Events normalized to unity')
    h.SetTitle('')
#    h.SetTitle(titlelib[hist[1:]])

    h.Draw('hist e1')
    h2.Draw('histsame e1')
#    leg.SetFillStyle(0)
    leg.Draw()
    stamp()
    c1.Update()
    fnew.cd()
    c1.Write(legHeader.replace(' ','_'))
    #pause()
    c1.Print('compHist_pdf/'+pdfname.replace(' ','_')+'.png')
    print 'created:' ,'compHist_pdf/'+pdfname.replace(' ','_')+'.png'
print 'just made', fnew.GetName()
fnew.Close()
exit(0)
