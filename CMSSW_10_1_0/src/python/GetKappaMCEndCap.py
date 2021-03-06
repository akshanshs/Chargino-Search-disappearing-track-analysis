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
m = [15, 30, 50, 70, 90, 120, 200, 300, 310]
eta = [0,1.4442,1.566,2.4]

hHTnum                          = TH1F("hHTnum","HT for number of events", 150,40,2500)
histoStyler(hHTnum,1)
hnJets                          = TH1F("hnJets", "Jet multiplicity", 8, 0, 8)
histoStyler(hnJets,1)
hHT                             = TH1F("hHT","HT", 150,40,2500)
histoStyler(hHT,1)
hMETpf                          = TH1F("hMETpf","pfMET", 150,30,1000)
histoStyler(hMETpf,1)
hnGenE                            = TH1F("hnGenE", "number of generated electrons", 4, 0, 4)
histoStyler(hnGenE,1)

hnDT                            = TH1F("hnDT", "number of disappearing tracks", 4, 0, 4)
histoStyler(hnDT,1)
hSnDT                            = TH1F("hSnDT", "number of disappearing tracks", 4, 0, 4)
histoStyler(hSnDT,1)
hMnDT                            = TH1F("hMnDT", "number of disappearing tracks", 4, 0, 4)
histoStyler(hMnDT,1)
hLnDT                            = TH1F("hLnDT", "number of disappearing tracks", 4, 0, 4)
histoStyler(hLnDT,1)
hMHT                            = TH1F("hMHT","MHT",100,40,1500)
histoStyler(hMHT,1)

hMHT                            = TH1F("hMHT","MHT",100,40,1500)
histoStyler(hMHT,1)
####
hEleGenPtRECOeff      = TH1D("hEleGenPtRECOeff", ";m [GeV] ;pt of the RECO Ele;;", len(m)-1,np.asarray(m, 'd'))
histoStyler(hEleGenPtRECOeff,1)
hEleGenPtDTeff        = TH1D("hEleGenPtDTeff", "pt of the DT Ele", len(m)-1,np.asarray(m, 'd'))
histoStyler(hEleGenPtDTeff,1)
hEleGenPtSDTeff        = TH1D("hEleGenPtSDTeff", "pt of the SDT Ele", len(m)-1,np.asarray(m, 'd'))
histoStyler(hEleGenPtSDTeff,1)
hEleGenPtMDTeff        = TH1D("hEleGenPtMDTeff", "pt of the MDT Ele", len(m)-1,np.asarray(m, 'd'))
histoStyler(hEleGenPtMDTeff,1)
hEleGenPtLDTeff        = TH1D("hEleGenPtLDTeff", "pt of the LDT Ele", len(m)-1,np.asarray(m, 'd'))
histoStyler(hEleGenPtLDTeff,1)
hEleGenEta            = TH1D("hEleGenEta", "Eta of the gen Ele", len(eta)-1,np.asarray(eta, 'd'))
histoStyler(hEleGenEta,1)
hEleGenEtaRECOeff     = TH1D("hEleGenEtaRECOeff", "Eta of the gen Ele", len(eta)-1,np.asarray(eta, 'd'))
histoStyler(hEleGenEtaRECOeff,1)
hEleGenEtaDTeff       = TH1D("hEleGenEtaDTeff", "Eta of the reco Ele", len(eta)-1,np.asarray(eta, 'd'))
histoStyler(hEleGenEtaDTeff,1)
hEleGenEtaSDTeff       = TH1D("hEleGenEtaSDTeff", "Eta of the SDT", len(eta)-1,np.asarray(eta, 'd'))
histoStyler(hEleGenEtaSDTeff,1)
hEleGenEtaMDTeff       = TH1D("hEleGenEtaMDTeff", "Eta of the MDT", len(eta)-1,np.asarray(eta, 'd'))
histoStyler(hEleGenEtaMDTeff,1)
hEleGenEtaLDTeff       = TH1D("hEleGenEtaLDTeff", "Eta of the LDT", len(eta)-1,np.asarray(eta, 'd'))
histoStyler(hEleGenEtaLDTeff,1)

htrkresp              = TH1D("htrkresp","track response", 50,-3,3.2)
histoStyler(htrkresp,1)
htrkrespS              = TH1D("htrkrespS","small track response", 50,-3,3.2)
histoStyler(htrkrespS,1)
htrkrespM              = TH1D("htrkrespM","medium track response", 50,-3,3.2)
histoStyler(htrkrespM,1)
htrkrespL              = TH1D("htrkrespL","long track response", 50,-3,3.2)
histoStyler(htrkrespL,1)
hmuonresp             =TH1D("hmuonresp","muon response", 50,-3,3.2)
histoStyler(hmuonresp,1)

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
        hHTnum.Fill(c.madHT)
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
            if not abs(muon.Eta()) > 1.566 and abs(muon.Eta()) < 2.4: continue
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

            if not (gen.Pt() > 10 and abs(gen.Eta()) < 2.4 and abs(gen.Eta()) > 1.566): continue
            if not (abs(c.GenParticles_PdgId[igen]) == 11 and c.GenParticles_Status[igen] == 1): continue
#            print 'Parent Id is', c.GenParticles_ParentId[igen]
            nGenE += 1
#            if nGenE >2: 
#                print 'number of Gen electrons', nGenE
#                pause()
            for im, m in enumerate(c.Electrons):
                if not (m.Pt() > 10 and abs(m.Eta()) < 2.4 and abs(m.Eta()) > 1.566 ): continue
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

            if drsmall < .01:
                hEleGenPtRECOeff.Fill(c.Electrons[idlep].Pt(), (c.CrossSection*35.9)/(1*.001))
                hEleGenEtaRECOeff.Fill(abs(c.Electrons[idlep].Eta()), (c.CrossSection*35.9)/(1*.001))
                hmuonresp.Fill(math.log10(c.Electrons[idlep].Pt()/gen.Pt()),(c.CrossSection*35.9)/(1*.001))

            for itrk, trk in enumerate(c.tracks):
                if not (trk.Pt() > 15 and abs(trk.Eta()) > 1.566 and abs(trk.Eta()) < 2.4): continue
                if not isBaselineTrack(trk, itrk): continue
                if not isDisappearingTrack(trk, itrk): continue
                dr = gen.DeltaR(trk)
                if dr < drsmal:
                    drsmal = dr
                    idtrk   = itrk
                    trkTlvsum = trk
            if drsmal < 0.01:
                dtTlvsum = trkTlvsum
                nDT +=1
                hEleGenPtDTeff.Fill(c.tracks[idtrk].Pt(), (c.CrossSection*35.9)/(1*.001))
                hEleGenEtaDTeff.Fill(abs(c.tracks[idtrk].Eta()), (c.CrossSection*35.9)/(1*.001))
                htrkresp.Fill(math.log10(c.tracks[idtrk].Pt()/gen.Pt()),(c.CrossSection*35.9)/(1*.001))
                length = determineSML(dtTlvsum, idtrk)
                if (length == 1):
                    SnDT += 1
                    htrkrespS.Fill(math.log10(c.tracks[idtrk].Pt()/gen.Pt()),(c.CrossSection*35.9)/(1*.001))
                    hEleGenPtSDTeff.Fill(c.tracks[idtrk].Pt(), (c.CrossSection*35.9)/(1*.001))
                    hEleGenEtaSDTeff.Fill(abs(c.tracks[idtrk].Eta()), (c.CrossSection*35.9)/(1*.001))
                if (length == 2):
                    MnDT += 1
                    htrkrespM.Fill(math.log10(c.tracks[idtrk].Pt()/gen.Pt()),(c.CrossSection*35.9)/(1*.001))
                    hEleGenPtMDTeff.Fill(c.tracks[idtrk].Pt(), (c.CrossSection*35.9)/(1*.001))
                    hEleGenEtaMDTeff.Fill(abs(c.tracks[idtrk].Eta()), (c.CrossSection*35.9)/(1*.001))
                if (length == 3):
                    LnDT += 1
                    htrkrespL.Fill(math.log10(c.tracks[idtrk].Pt()/gen.Pt()),(c.CrossSection*35.9)/(1*.001))
                    hEleGenPtLDTeff.Fill(c.tracks[idtrk].Pt(), (c.CrossSection*35.9)/(1*.001))
                    hEleGenEtaLDTeff.Fill(abs(c.tracks[idtrk].Eta()), (c.CrossSection*35.9)/(1*.001))

        hnGenE.Fill(nGenE, (c.CrossSection*35.9)/(1*.001))
        hnDT.Fill(nDT, (c.CrossSection*35.9)/(1*.001))
        #print nDT
        if (nDT > 0):
            #print 'after if', nDT
            hSnDT.Fill(SnDT, (c.CrossSection*35.9)/(1*.001))
            hMnDT.Fill(MnDT, (c.CrossSection*35.9)/(1*.001))
            hLnDT.Fill(LnDT, (c.CrossSection*35.9)/(1*.001))
            hHT.Fill(c.HT, (c.CrossSection*35.9)/(1*.001))
            hnJets.Fill(c.NJets, (c.CrossSection*35.9)/(1*.001))
            hMETpf.Fill(c.MET, (c.CrossSection*35.9)/(1*.001))
            hMHT.Fill(c.MHT, (c.CrossSection*35.9)/(1*.001))
    fnew = TFile('BkgHists_'+identifier+'.root','recreate')
    fnew.cd()
    hHTnum.Write()
    hnGenE.Write()
    hnDT.Write()
    hSnDT.Write()
    hMnDT.Write()
    hLnDT.Write()
    hHT.Write()
    hnJets.Write()
    hMETpf.Write()
#    hMHT.Write()

    hEleGenPtRECOeff.Write()
    hEleGenEtaRECOeff.Write()

    hEleGenPtDTeff.Write()
    hEleGenEtaDTeff.Write()
    hEleGenPtSDTeff.Write()
    hEleGenEtaSDTeff.Write()
    hEleGenPtMDTeff.Write()
    hEleGenEtaMDTeff.Write()
    hEleGenPtLDTeff.Write()
    hEleGenEtaLDTeff.Write()
    htrkresp.Write()
    htrkrespS.Write()
    htrkrespM.Write()
    htrkrespL.Write()
    hmuonresp.Write()

    print "Just created", fnew.GetName()
    fnew.Close()

    ftem = TFile('Template_Hists'+identifier+'.root','recreate')
    ftem.cd()
    htrkresp.Write()
    htrkrespS.Write()
    htrkrespM.Write()
    htrkrespL.Write()
    hmuonresp.Write()
    ftem.Close()
    print "file:", ftem, "created."
    


def determineSML(sp_chi, sp_chi_id):
    S = 0
    M = 0
    L = 0
    if c.tracks_pixelLayersWithMeasurement[sp_chi_id] == c.tracks_trackerLayersWithMeasurement[sp_chi_id]: S = 1
    if c.tracks_trackerLayersWithMeasurement[sp_chi_id] < 7 and c.tracks_pixelLayersWithMeasurement[sp_chi_id] < c.tracks_trackerLayersWithMeasurement[sp_chi_id]: M = 2
    if c.tracks_trackerLayersWithMeasurement[sp_chi_id] > 6 and c.tracks_pixelLayersWithMeasurement[sp_chi_id] < c.tracks_trackerLayersWithMeasurement[sp_chi_id]: L = 3
    return S+M+L

def isBaselineTrack(track, track_id):
    flag = 1
    if not (track.Pt()>10 and abs(track.Eta())<2.4 and abs(track.Eta()) > 1.566): return 0
    if not bool(c.tracks_trackQualityHighPurity[track_id]) : return 0
    if not (c.tracks_ptError[track_id]/(track.Pt()*track.Pt()) < 0.2): return 0
    if not c.tracks_dxyVtx[track_id] < 0.02: return 0
    if not c.tracks_dzVtx[track_id] < 0.05 : return 0
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
    if c.tracks_dxyVtx[track_id] > 0.02 and S == 1: return 0
    if c.tracks_dxyVtx[track_id] > 0.01 and S == 0: return 0
    if c.tracks_neutralPtSum[track_id] > 10 or ((c.tracks_neutralPtSum[track_id]/track.Pt()) > 0.1): return 0
    if c.tracks_chargedPtSum[track_id] > 10 or ((c.tracks_chargedPtSum[track_id]/track.Pt()) > 0.1): return 0
    if not c.tracks_passPFCandVeto[track_id]:return 0
    if c.tracks_nMissingOuterHits[track_id] < 2 and S == 0: return 0
    if c.tracks_ptError[track_id]/(track.Pt()*track.Pt()) > 0.2 and S == 1: return 0
    if c.tracks_ptError[track_id]/(track.Pt()*track.Pt()) > 0.05 and M == 2: return 0
    if c.tracks_ptError[track_id]/(track.Pt()*track.Pt()) > 0.005 and L == 3: return 0
    return flag

main()
