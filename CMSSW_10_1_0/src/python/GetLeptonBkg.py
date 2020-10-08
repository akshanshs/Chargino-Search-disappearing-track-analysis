from ROOT import *
import sys
import numpy as np
from DataFormats.FWLite import Events, Handle
import scipy.constants as scc
import math
from glob import glob
from FWCore.ParameterSet.VarParsing import VarParsing
from random import shuffle
from utils import *

gROOT.SetBatch()
gROOT.SetStyle('Plain')

#fkappa = '/nfs/dust/cms/user/singha/LLCh/BACKGROUND/CMSSW_8_0_20/src/TagProbeTrees/TemplateSplit.root'
#f  = TFile(fkappa)
#keys = f.GetListOfKeys()
#sfHist   = f.Get('htrkrespL') #update

hHTnum                          = TH1F("hHTnum","HT for number of events", 150,40,2500)
histoStyler(hHTnum,1)
hnJets                          = TH1F("hnJets", "Jet multiplicity", 8, 0, 8)
histoStyler(hnJets,1)
hHT                             = TH1F("hHT","HT", 150,40,2500)
histoStyler(hHT,1)
hMETpf                          = TH1F("hMETpf","pfMET", 150,30,1000)
histoStyler(hMETpf,1)
hnDT                            = TH1F("hnDT", "number of disappearing tracks", 4, 0, 4)
histoStyler(hnDT,1)
hMHT                            = TH1F("hMHT","MHT",100,40,1500)
histoStyler(hMHT,1)

####
options = VarParsing ('python')
options.parseArguments()

#Input File    
inputFiles = options.inputFiles
if inputFiles == []:
    print 'running on the default'
    inputFiles = ["/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v1/Summer16.WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1_95_RA2AnalysisTree.root"]

c=TChain("TreeMaker2/PreSelection")
c.Add(inputFiles[0])

nentries = c.GetEntries()
print "will process", nentries, "events"

#Output file   

identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('pMSSM12_MCMC1_','pMSSMid').replace('_step4','').replace('_miniAODSIM','').replace('nFiles1_RA2AnalysisTree','').replace('_*','').replace('*','')

identifier+='nFiles'+str(len(inputFiles))

def main():

    for ientry in range(nentries):
        c.GetEntry(ientry)
        hHTnum.Fill(c.madHT)
        flag_probe = -1
        nDT = 0
        trkTlvsum = TLorentzVector()
        trkTlvsum.SetPxPyPzE(0, 0, 0, 0)

        for igen, gen in enumerate(c.GenParticles):
            drsmall = 0.2
            idtrk   = -1

            if not (gen.Pt() > 10 and abs(gen.Eta() < 2.4)): continue
            if not (abs(c.GenParticles_PdgId[igen]) == 11 and c.GenParticles_Status[igen] == 1): continue

            for itrk, trk in enumerate(c.tracks):
                if trk.Pt() < 10: continue
                dr = gen.DeltaR(trk)
                if dr < drsmall:
                    drsmall = dr
                    idtrk   = itrk
                    trkTlvsum = trk
                if drsmall < 0.01:
                    flag_probe = probe(trkTlvsum, idtrk)
                    if (flag_probe == 1):
                        nDT +=1
        hnDT.Fill(nDT, (c.CrossSection*35.9)/(1*.001))
        hHT.Fill(c.HT, (c.CrossSection*35.9)/(1*.001))
        hnJets.Fill(c.NJets, (c.CrossSection*35.9)/(1*.001))
        hMETpf.Fill(c.MET, (c.CrossSection*35.9)/(1*.001))
        hMHT.Fill(c.MHT, (c.CrossSection*35.9)/(1*.001))
    fnew = TFile('BkgHists_'+identifier+'.root','recreate')
    fnew.cd()
    hnDT.Write()
    hHT.Write()
    hnJets.Write()
    hMETpf.Write()
    hMHT.Write()
    
    print "Just created", fnew.GetName()
    fnew.Close()

def probe(chi, chi_id):

    S = 0
    M = 0
    L = 0
    flag = 1
    if not (chi.Pt() > 10): flag = 0
    if c.tracks_pixelLayersWithMeasurement[chi_id] == c.tracks_trackerLayersWithMeasurement[chi_id]: S = 1
    if c.tracks_trackerLayersWithMeasurement[chi_id] < 7 and c.tracks_pixelLayersWithMeasurement[chi_id] < c.tracks_trackerLayersWithMeasurement[chi_id] : M = 2
    if c.tracks_trackerLayersWithMeasurement[chi_id] > 6 and c.tracks_pixelLayersWithMeasurement[chi_id] < c.tracks_trackerLayersWithMeasurement[chi_id]: L = 3
    if chi.Pt() < 15 or abs(chi.Eta()) > 2.4 : flag = 0
    if c.tracks_dxyVtx[chi_id] > 0.02 and S == 1: flag = 0
    if c.tracks_dxyVtx[chi_id] > 0.01 and S == 0: flag = 0
    if c.tracks_dzVtx[chi_id]  > 0.05 : flag = 0
    if c.tracks_neutralPtSum[chi_id] > 10 or ((c.tracks_neutralPtSum[chi_id]/chi.Pt()) > 0.1): flag = 0
    if c.tracks_chargedPtSum[chi_id] > 10 or ((c.tracks_chargedPtSum[chi_id]/chi.Pt()) > 0.1): flag = 0
    if not c.tracks_passPFCandVeto[chi_id]:flag = 0
    if not (c.tracks_trkRelIso[chi_id] < 0.2): flag = 0
    if not (c.tracks_trkRelIso[chi_id]*chi.Pt() < 10) : flag = 0
    if c.tracks_trackerLayersWithMeasurement[chi_id] < 2 or c.tracks_nValidTrackerHits[chi_id] < 2 : flag = 0
    if c.tracks_nMissingInnerHits[chi_id] > 0: flag = 0
    if c.tracks_nMissingOuterHits[chi_id] < 2 and S == 0: flag = 0
    if c.tracks_ptError[chi_id]/(chi.Pt()*chi.Pt()) > 0.2 and S == 1: flag = 0
    if c.tracks_ptError[chi_id]/(chi.Pt()*chi.Pt()) > 0.05 and M == 2: flag = 0
    if c.tracks_ptError[chi_id]/(chi.Pt()*chi.Pt()) > 0.005 and L == 3: flag = 0
    if not c.tracks_trackQualityHighPurity[chi_id] : flag = 0
    return flag

main()
