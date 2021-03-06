from ROOT import *
from utilitiesII import *
#from utilsII import *
import os, sys
from glob import glob
gStyle.SetOptStat(0)
gROOT.SetBatch(1)

try: fname = sys.argv[1]
except: fname = 'test.root'

#Vars = ['Pt','eta','dxy','dz','sumNpt','sumCpt' ,'rsumNpt','rsumCpt','calodep','rIso', 'ohits','pterr','mihits','length'] #,'pterr']
track_category = ['inclusive','small','medium','long']
Vars = ['Pt','MET','HT','MHT','dPhiMin','dPhiMax','dPhimaxjets','dPhijet1','dPhi','mhtdPhi','R','mhtR','nJets','nbJets','nDtrks', 'nVtx']
pdgId = [['other', 46],['15',6],['13',2],['11',4],['0', 7]] # [pdgID, KColor]
particle = {pdgId[0][0]:'other',pdgId[1][0]:'prompt (#tau^{#pm})', pdgId[2][0]:'prompt (#mu^{#pm})', pdgId[3][0]:'prompt (e^{#pm})', pdgId[4][0]:'non-prompt'}
infile = TFile(fname)
infile.ls()


#region =    'SBCRden' #'MBSRnum' #'MBCRden' #'MBSRnum' #'SBSRnum' # 'SBCRden'
fnew = TFile('newfile.root','recreate')

if 'SB_' in fname: regions = ['SBCRden','SBSRnum']
if 'MB_' in fname: regions = ['MBCRden','MBSRnum']

#regions = ['SBCRden', 'SBSRnum','MBCRden','MBSRnum']
dBkgCompositionHist = {}
dSigCompositionHist = {}
for iregion, region in enumerate(regions):
    
    for ivar, var in enumerate(Vars):
        for icategory, category in enumerate(track_category):

            newHistKey = 'Bkg'+category+'_'+var+'_'+region+"comp"
            dBkgCompositionHist[newHistKey] = THStack(newHistKey,"")
            c1 = mkcanvas(newHistKey)
            if (('length' not in var)  and ('R' not in var) and ('nDtrks' not in var)) and ('dPhi' not in var) : c1.SetLogy()
#        c1.SetLogy()
            leg = mklegend(x1=.63, y1=.69, x2= 0.99, y2=.91, color=kWhite)
            maxy = 1
            miny = 10000
    
            for ipdg, pdg in enumerate(pdgId):
#        if ipdg == 0: continue
                histname = 'Bkg'+category+'_'+var+'_'+region+'_'+pdg[0]
                print histname
                if ('length' not in histname)  and ('R' not in histname) and ('nDtrks' not in histname) and ('dPhi' not in histname) : c1.SetLogy()
                hist = infile.Get(histname)
#        overflow(hist)
#        print hist
                if miny > hist.GetMinimum() and hist.GetMinimum() > 0: miny = hist.GetMinimum()
                if maxy < hist.GetMaximum(): maxy = hist.GetMaximum()
            
                color = pdg[1]
                hist.SetFillColor(color)
                hist.SetLineColor(1)
                hist.SetLineWidth(1)
                hist.SetMarkerColor(color)
                leg.AddEntry(hist,particle[pdg[0]],'f')
                dBkgCompositionHist[newHistKey].Add(hist)

            if ('length' not in var) and ('nDtrks' not in var)  and ('R' not in var) and ('dPhi' not in var): maxy = 100*maxy
            else: maxy = 5*maxy
            c1.Update()
            c1.cd(1)
            dBkgCompositionHist[newHistKey].Draw("hist")
#    dSigCompositionHist[newHistKeySig].Draw("nostack")
#    dBkgCompositionHist[newHistKey].GetYaxis().SetRangeUser(0.01,maxy)
            dBkgCompositionHist[newHistKey].GetXaxis().SetTitle(namewizard(var))
            dBkgCompositionHist[newHistKey].GetYaxis().SetTitleOffset(1)
            dBkgCompositionHist[newHistKey].GetXaxis().SetTitleOffset(1)
            dBkgCompositionHist[newHistKey].GetYaxis().SetTitle('Number of events')
            dBkgCompositionHist[newHistKey].GetXaxis().SetLabelSize(.045)
            dBkgCompositionHist[newHistKey].GetYaxis().SetTitleSize(.05)
            dBkgCompositionHist[newHistKey].GetXaxis().SetTitleSize(.05)

#    if miny > 0: dBkgCompositionHist[newHistKey].SetMinimum(miny)
#    else:
            if 'mihits' in var: miny = .001
            else: miny = 0.1
            dBkgCompositionHist[newHistKey].SetMinimum(miny)
            dBkgCompositionHist[newHistKey].SetMaximum(maxy)
            leg.Draw()
            stamp2fig()
            c1.Update()
            outputfolder = region.replace('num','').replace('den','')
            if 'inclusive' in newHistKey: c1.Print('pdfs/fakehists/'+outputfolder+'/inclusive/'+newHistKey+'.png')
            if 'small' in newHistKey: c1.Print('pdfs/fakehists/'+outputfolder+'/short/'+newHistKey+'.png')
            if 'medium' in newHistKey: c1.Print('pdfs/fakehists/'+outputfolder+'/medium/'+newHistKey+'.png')
            if 'long' in newHistKey: c1.Print('pdfs/fakehists/'+outputfolder+'/long/'+newHistKey+'.png')
#        c1.Print('pdfs/bkgevents/'+newHistKey+'.pdf')

        
