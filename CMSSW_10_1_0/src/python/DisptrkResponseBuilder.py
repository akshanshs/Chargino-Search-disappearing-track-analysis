from ROOT import *
import sys
import numpy as np
from DataFormats.FWLite import Events, Handle
import scipy.constants as scc
import math
from glob import glob
from FWCore.ParameterSet.VarParsing import VarParsing
from random import shuffle
#from utils import *
from utilsII import *

gROOT.SetBatch()
gROOT.SetStyle('Plain')


dResponseHist = {}
for iPtBin, PtBin in enumerate(PtBinEdges[:-1]):
	for iEtaBin, EtaBin in enumerate(EtaBinEdges[:-1]):
		newHistKey = ((EtaBin,EtaBinEdges[iEtaBin + 1]),(PtBin,PtBinEdges[iPtBin + 1]))
		dResponseHist[newHistKey] = TH1D("htrkresp"+str(newHistKey),"htrkresp"+str(newHistKey), 200,-2,2)
		histoStyler(dResponseHist[newHistKey], 1)

dEleResponseHist = {}
for iPtBin, PtBin in enumerate(PtBinEdges[:-1]):
        for iEtaBin, EtaBin in enumerate(EtaBinEdges[:-1]):
                newHistKey = ((EtaBin,EtaBinEdges[iEtaBin + 1]),(PtBin,PtBinEdges[iPtBin + 1]))
                dEleResponseHist[newHistKey] = TH1D("heleresp"+str(newHistKey),"heleresp"+str(newHistKey), 200,-2,2)
                histoStyler(dEleResponseHist[newHistKey], 1)


####
options = VarParsing ('python')
options.parseArguments()

#Input File    
inputFiles = options.inputFiles
if inputFiles == []:
    print 'running on the default'
    inputFiles = ["/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1_391_RA2AnalysisTree.root"]

c=TChain("TreeMaker2/PreSelection")
x = len(inputFiles)
#c.Add(inputFiles[0])

nentries = c.GetEntries()
print "will process", nentries, "events"

#Output file   
verbosity = 1000
identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('pMSSM12_MCMC1_','pMSSMid').replace('_step4','').replace('_miniAODSIM','').replace('nFiles1_RA2AnalysisTree','').replace('_*','').replace('*','')

identifier+='nFiles'+str(len(inputFiles))

def main():

    for f in range(0,x):
        print 'file number:', f, ':',inputFiles[f]
        c.Add(inputFiles[f])

    nentries = c.GetEntries()
    print "will process", nentries, "events"
    for ientry in range(nentries):
        if ientry%verbosity ==0:
            print 'Now processing event number', ientry
        c.GetEntry(ientry)
        weight = 1
#	if not (c.HT > 100): continue
#        if not(c.NJets > 1 and c.NJets < 4): continue
        flag_probe = -1
        nGenE = 0
        nDT = 0
        SnDT = 0
        MnDT = 0
        LnDT = 0
        trkTlvsum = TLorentzVector()
        trkTlvsum.SetPxPyPzE(0, 0, 0, 0)
        dtTlvsum = TLorentzVector()
        dtTlvsum.SetPxPyPzE(0, 0, 0, 0)
        
        muons = []
        for imu, muon in enumerate(c.Muons):
            if not muon.Pt() > 15: continue
            if not (abs(muon.Eta()) < 2.4): continue
            if  abs(muon.Eta()) > 1.4442 and abs(muon.Eta()) < 1.566: continue
            muons.append(muon)
        if not len(muons)==0: continue

        basicTracks = []
        for itrack, track in enumerate(c.tracks):
            if not isBaselineTrack(track, itrack): continue
            basicTracks.append(track)
        
        for igen, gen in enumerate(c.GenParticles):
            drsmall = 0.2
            drsmal  = 0.2
            idtrk   = -1
            idlep   = -1

            if not (gen.Pt() > 3 and abs(gen.Eta()) < 2.4): continue
            if not (abs(c.GenParticles_PdgId[igen]) == 11 and c.GenParticles_Status[igen] == 1): continue
            if (abs(gen.Eta()) > 1.4442 and abs(gen.Eta()) < 1.566) : continue
            nGenE += 1

            for im, m in enumerate(c.Electrons):
                if (abs(m.Eta()) < 1.566 and abs(m.Eta()) > 1.4442): continue        
                if not (m.Pt() > 10 and abs(m.Eta()) < 2.4): continue
		if not c.Electrons_passIso[im]: continue
                drBig4Trk = 9999
                for trk in basicTracks:
                    drTrk = trk.DeltaR(c.Electrons[im])
                    if drTrk<drBig4Trk:
                        drBig4Trk = drTrk
                        if drTrk<0.01: break
                if not drBig4Trk<0.01: continue
                
                dr = gen.DeltaR(m)

                if dr < drsmall:
                    drsmall = dr
                    idlep   = im
#            print gen.Eta()
            if drsmall < .005:
		    for histkey in  dEleResponseHist:
			    if abs(c.Electrons[idlep].Eta()) > histkey[0][0] and abs(c.Electrons[idlep].Eta()) < histkey[0][1] and gen.Pt() > histkey[1][0] and min(gen.Pt(),2009.999) < histkey[1][1]:
				    fillth1(dEleResponseHist[histkey],math.log10(c.Electrons[idlep].Pt()/gen.Pt()),weight)




	    for itrk, trk in enumerate(c.tracks):
                if (abs(trk.Eta()) < 1.566 and abs(trk.Eta()) > 1.4442): continue            
                if not (trk.Pt() > 3 and abs(trk.Eta()) < 2.4): continue
                if not isBaselineTrack(trk, itrk): continue
                if not isDisappearingTrack(trk, itrk): continue
                dr = gen.DeltaR(trk)
                if dr < drsmal:
                    drsmal = dr
                    idtrk   = itrk
                    trkTlvsum = trk
            if drsmal < 0.005:
                dtTlvsum = trkTlvsum
                nDT +=1
		print 'found disappearing track eta:', abs(c.tracks[idtrk].Eta()), 'Pt:', gen.Pt()
                for histkey in  dResponseHist:
                    if abs(c.tracks[idtrk].Eta()) > histkey[0][0] and abs(c.tracks[idtrk].Eta()) < histkey[0][1] and gen.Pt() > histkey[1][0] and min(gen.Pt(),2009.999) < histkey[1][1]:
			    fillth1(dResponseHist[histkey],math.log10(c.tracks[idtrk].Pt()/gen.Pt()),weight)                


    ftem = TFile('BinnedTemplate_Hists'+identifier+'.root','recreate')
    ftem.cd()

    for histkey in  dResponseHist: dResponseHist[histkey].Write()
    for histkey in  dEleResponseHist: dEleResponseHist[histkey].Write()
    ftem.Close()
    print "file:", ftem, "created."
    
def isBaselineTrack(track, track_id):
    flag = 1
#    if not (track.Pt()> 10 and abs(track.Eta())<2.4): return 0
    if abs(track.Eta()) < 1.566 and abs(track.Eta()) > 1.4442: return 0
    if not bool(c.tracks_trackQualityHighPurity[track_id]) : return 0
    if not (c.tracks_ptError[track_id]/(track.Pt()*track.Pt()) < 0.2): return 0
    if not c.tracks_dxyVtx[track_id] < 0.01: return 0
    if not c.tracks_dzVtx[track_id] < 0.02 : return 0
    if not c.tracks_trkRelIso[track_id] < 0.2: return 0
    if not c.tracks_trkRelIso[track_id]*track.Pt() < 10: return 0
    if not (c.tracks_trackerLayersWithMeasurement[track_id] >= 2 and c.tracks_nValidTrackerHits[track_id] >= 2): return 0
    if not c.tracks_nMissingInnerHits[track_id]==0: return 0
    return flag

def isDisappearingTrack(track, track_id):
    S = 0
    M = 0
    L = 0
    flag = 1
    if c.tracks_pixelLayersWithMeasurement[track_id] == c.tracks_trackerLayersWithMeasurement[track_id]: S = 1
    if c.tracks_trackerLayersWithMeasurement[track_id] < 7 and c.tracks_pixelLayersWithMeasurement[track_id] < c.tracks_trackerLayersWithMeasurement[track_id] : M = 2
    if c.tracks_trackerLayersWithMeasurement[track_id] > 6 and c.tracks_pixelLayersWithMeasurement[track_id] < c.tracks_trackerLayersWithMeasurement[track_id]: L = 3
#    if track.Pt() < 15: return 0
    if not muonVeto(track): return 0
    if not electronVeto(track): return 0
    if c.tracks_dxyVtx[track_id] > 0.01 and S == 1: return 0
    if c.tracks_dxyVtx[track_id] > 0.01 and S == 0: return 0
    if c.tracks_matchedCaloEnergy[track_id] > 10: return 0
    if c.tracks_neutralPtSum[track_id] > 10 or ((c.tracks_neutralPtSum[track_id]/track.Pt()) > 0.1): return 0
    if c.tracks_chargedPtSum[track_id] > 10 or ((c.tracks_chargedPtSum[track_id]/track.Pt()) > 0.1): return 0
    if not c.tracks_passPFCandVeto[track_id]:return 0
    if c.tracks_nMissingOuterHits[track_id] < 2 and S == 0: return 0
    if c.tracks_ptError[track_id]/(track.Pt()*track.Pt()) > 0.2 and S == 1: return 0
    if c.tracks_ptError[track_id]/(track.Pt()*track.Pt()) > 0.05 and M == 2: return 0
    if c.tracks_ptError[track_id]/(track.Pt()*track.Pt()) > 0.02 and L == 3: return 0
    return flag



def muonVeto(trkTlv):
    flag = True
    dr = 4
    for imu, mu in enumerate(c.Muons):
        if mu.Pt() < 10:continue
        try:
            dr = trkTlv.DeltaR(mu)
        except:
            dr = 4
        if dr < 0.15:
            flag = False
            break
    return flag

def electronVeto(trkTlv):
    flag = True
    dr = 4
    for iele, electron in enumerate(c.Electrons):
        if electron.Pt() < 10:continue
        try:
            dr = trkTlv.DeltaR(electron)
        except:
            dr = 4
        if dr < 0.15:
            flag = False
            break
    return flag





main()
