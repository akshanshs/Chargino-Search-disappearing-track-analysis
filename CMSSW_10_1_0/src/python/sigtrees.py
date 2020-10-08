#! /usr/bin/env python

from ROOT import *
import sys
import numpy as np
from DataFormats.FWLite import Events, Handle
import scipy.constants as scc
import math
from glob import glob

gROOT.SetBatch()
gROOT.SetStyle('Plain')

# Make VarParsing object
# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideAboutPythonConfigFile#VarParsing_Example
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')
options.parseArguments()


def main():

    inputFiles = options.inputFiles
    if inputFiles == []:
        print 'running on default 100 events: sample cTau = 55 cm'
        inputFiles = ['/nfs/dust/cms/user/singha/LLCh/CMSSW_8_0_20/src/analysis/batch_test/pMSSM12_MCMC1_8_373637_step2_AODSIM_10of100.root']

#        inputFiles = ['/nfs/dust/cms/user/singha/MET_scan_8/CMSSW_8_0_20/src/MetScanning/LLPtupleTEST1/AODI/merged/pMSSM12_MCMC1_10_374794_step2_AODSIM.root']
    events = Events(inputFiles)

#basic track variables


    hPt                 = TH1F("hPt", "gen #chi^{#pm} Pt", 25, 0, 1000)
    hValidHitsDT        = TH1F("hValidHitsDT","number of valid hits^{#DeltaR(#chi^{#pm},track)<0.01}", 15, 0 ,30)
    hInnerMissDT        = TH1F("hInnerMissDT","missing inner hits^{#DeltaR(#chi^{#pm},track)<0.01}", 15, 0 ,15)
    hMiddleMissDT       = TH1F("hMiddleMissDT","missing middle hits^{#DeltaR(#chi^{#pm},track)<0.01}", 15, 0, 15)
    hOuterMissDT        = TH1F("hOuterMissDT","missing outer hits^{#DeltaR(#chi^{#pm},track)<0.01}",15, 0, 15)
    htrkHits            = TH1F("htrkHits","number of tracker hits^{#DeltaR(#chi^{#pm},track)<0.01}", 30, 0 ,30)
    hpixHits            = TH1F("hpixHits","number of pixel hits^{#DeltaR(#chi^{#pm},track)<0.01}", 8, 0 ,8)
    hpixBHits           = TH1F("hpixBHits","number of pixel barrel hits^{#DeltaR(#chi^{#pm},track)<0.01}", 5, 0 ,5)
    hpixECHits          = TH1F("hpixECHits","number of pixel end cap hits^{#DeltaR(#chi^{#pm},track)<0.01}", 4, 0 ,4)

    hrelisop3           = TH1F("hrelisop3", "RelIso #DeltaR < 0.3 ", 30, -0.0001, 0.5)
    hminIso             = TH1F("hminIso", "mini Isolation ", 30, -0.0001, 0.5)




#    f    = TFile('signaltrk'+identifier+'.root','recreate')       #file with signal tree
    t    = TTree('Analysis','Analysis')          #tree for optimization variables

    weight      = np.zeros(1, dtype = float)
    b_weight    = t.Branch('weight', weight, 'weight/D')

    inMiss      = np.zeros(1, dtype = int)
    b_inMiss    = t.Branch('inMiss', inMiss, 'inMiss/I')

    midMiss     = np.zeros(1, dtype = int)
    b_midMiss   = t.Branch('midMiss', midMiss, 'midMiss/I')

    outMiss     = np.zeros(1, dtype = int)
    b_outMiss   = t.Branch('outMiss', outMiss, 'outMiss/I')

    pixHits     = np.zeros(1, dtype = int)
    b_pixHits   = t.Branch('pixHits', pixHits, 'pixHits/I')
    pixHitsB     = np.zeros(1, dtype = int)
    b_pixHitsB   = t.Branch('pixHitsB', pixHitsB, 'pixHitsB/I')
    pixHitsEC     = np.zeros(1, dtype = int)
    b_pixHitsEC   = t.Branch('pixHitsEC', pixHitsEC, 'pixHitsEC/I')

    validHits   = np.zeros(1, dtype = int)
    b_validHits = t.Branch('validHits', validHits, 'validHits/I')

    relIso      = np.zeros(1, dtype = float)
    b_relIso    = t.Branch('relIso', relIso, 'relIso/D')

    miniIso     = np.zeros(1, dtype = float)
    b_miniIso    = t.Branch('miniIso', miniIso, 'miniIso/D')

    ientry = 0


    handle_muons       = Handle ("std::vector<reco::Muon>")
    label_muons        = ('muons') 

    handle_electrons   = Handle ("vector<reco::GsfElectron>")
    label_electrons    = ('gedGsfElectrons')

    handle_tracks      = Handle ("vector<reco::Track>")
    label_tracks       = ('generalTracks')

    handle_pfcands     = Handle ("std::vector<reco::PFCandidate>")
    label_pfcands      = ('particleFlow')

    handle_genparticles= Handle ("vector<reco::GenParticle>")
    label_genparticles = ('genParticlePlusGeant')
    
    handle_jets        = Handle ("vector<reco::PFJet>")
    label_jets         = ('ak4PFJetsCHS')

    handle_MET         = Handle ("vector<reco::PFMET>")
    label_MET          = ('pfMet')

    


    for event in events:
        event.getByLabel (label_muons, handle_muons)
        event.getByLabel (label_electrons, handle_electrons)
        event.getByLabel (label_tracks, handle_tracks)
        event.getByLabel (label_genparticles, handle_genparticles)
        event.getByLabel (label_pfcands, handle_pfcands)
        event.getByLabel (label_MET, handle_MET)
        event.getByLabel (label_jets, handle_jets)

        muons          = handle_muons.product()
        electrons      = handle_electrons.product()
        tracks         = handle_tracks.product()
        genparticles   = handle_genparticles.product()
        pfcands        = handle_pfcands.product()
        MET            = handle_MET.product()
        jets           = handle_jets.product()

#        print tracks[0].appendTrackerHitPattern()
#        print dir(tracks[0].hitPattern())
#        exit(0)


        for gp in genparticles:
            if gp.pt() < 30 :continue # or abs(gp.eta()) > 1.0):continue 
            if abs(gp.pdgId())==1000024 and gp.status()==1:
                try:
                    log10decaylength = TMath.Log10(TMath.Sqrt(pow(gp.daughter(0).vx() - gp.vx(),2) + pow(gp.daughter(0).vy()-gp.vy(),2) ))
                except:
                    log10decaylength = -1.49
                
                chiTlv = TLorentzVector()
                chiTlv.SetPxPyPzE(gp.px(),gp.py(),gp.pz(),gp.energy())
                drmin = 2.0
                track_id = -1
                for itrack, track in enumerate(tracks):
                    if track.pt() < 15 or track.eta() > 0.9 : continue
                    trkTlv = TLorentzVector()
                    trkTlv.SetPxPyPzE(track.px(), track.py(), track.pz(), track.pt())
##==========VETOS=*=*=*=*=*                  # 0 if vetoed                                                                                                                         
                    DRmu  = drmu(trkTlv,muons)
                    DRele = drele(trkTlv,electrons)
                    DRjet = drjet(trkTlv,jets)
                    veto = DRmu and DRele and DRjet
                    if veto == 0:continue

                    dr = trkTlv.DeltaR(chiTlv)
                    if dr<drmin:
                        drmin = dr
                        track_id = itrack

######ISOLATION
                riso = reliso(tracks[track_id],tracks)
                miso = miniso(tracks[track_id],tracks)

#######Fill the tree
                if drmin < 0.01: #and veto:
                    if ientry%10==0: print 'filling tree: ', ientry # debug check
                    t.GetEntry(ientry)
                    weight[0]    = 1
                    validHits[0] = tracks[track_id].numberOfValidHits()
                    inMiss[0]    = tracks[track_id].hitPattern().trackerLayersWithoutMeasurement(reco.HitPattern.MISSING_INNER_HITS)   
                    midMiss[0]   = tracks[track_id].hitPattern().trackerLayersWithoutMeasurement(reco.HitPattern.TRACK_HITS)
                    outMiss[0]   = tracks[track_id].hitPattern().trackerLayersWithoutMeasurement(reco.HitPattern.MISSING_OUTER_HITS)
                    pixHits[0]   = tracks[track_id].hitPattern().pixelLayersWithMeasurement()
                    pixHitsB[0]  = tracks[track_id].hitPattern().pixelBarrelLayersWithMeasurement()
                    pixHitsEC[0] = tracks[track_id].hitPattern().pixelEndcapLayersWithMeasurement()
                    relIso[0]    = riso
                    miniIso[0]   = miso
                    ientry = ientry +1
                    
                    hValidHitsDT.Fill(tracks[track_id].numberOfValidHits())
                    hInnerMissDT.Fill(tracks[track_id].hitPattern().trackerLayersWithoutMeasurement(reco.HitPattern.MISSING_INNER_HITS))
                    hMiddleMissDT.Fill(tracks[track_id].hitPattern().trackerLayersWithoutMeasurement(reco.HitPattern.TRACK_HITS))
                    hOuterMissDT.Fill(tracks[track_id].hitPattern().trackerLayersWithoutMeasurement(reco.HitPattern.MISSING_OUTER_HITS))
                    hpixBHits.Fill(tracks[track_id].hitPattern().pixelBarrelLayersWithMeasurement())
                    hpixECHits.Fill(tracks[track_id].hitPattern().pixelEndcapLayersWithMeasurement())
                    hpixHits.Fill(tracks[track_id].hitPattern().pixelLayersWithMeasurement())
                    hrelisop3.Fill(riso)
                    hminIso.Fill(miso)
                    hPt.Fill(tracks[track_id].pt())
#                    print tracks[track_id].hitPattern().pixelLayersWithMeasurement()
#                    print tracks[track_id].hitPattern().numberOfValidPixelHits()
#                    print 10*'*='
                    t.Fill()




    identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('_step2','').replace('_AODSIM','').replace('_*','').replace('*','')
    identifier+='nFiles'+str(len(inputFiles))
#    f    = TFile('test.root','recreate')
    f    = TFile('signaltrk'+identifier+'.root','recreate')       #file with signal tree variables
    t.Write()
    f.Close()

    fhist = TFile('hists_'+identifier+'.root','recreate')  # root tree for histograms
    hPt.Write()
    hValidHitsDT.Write()
    hInnerMissDT.Write()
    hMiddleMissDT.Write()
    hOuterMissDT.Write()
    hpixBHits.Write()
    hpixECHits.Write()
    hpixHits.Write()
    hpixHits.Write()
    hrelisop3.Write()
    hminIso.Write()
    
#    t.Write()
#    f.Close()


def drmu(Tlv,muonlist = [], *args):
    flag = 1
    for muon in muonlist:
        if muon.pt() < 10:continue
        muonTlv = TLorentzVector()
        muonTlv.SetPxPyPzE(muon.px(),muon.py(),muon.pz(),muon.energy())
        dr = Tlv.DeltaR(muonTlv)
        if dr < 0.15:
            flag = 0
            break
#    print flag
    return flag

def drele(Tlv,electronlist = [], *args):
    flag = 1
    for electron in electronlist:
        if electron.pt() < 10:continue
        electronTlv = TLorentzVector()
        electronTlv.SetPxPyPzE(electron.px(),electron.py(),electron.pz(),electron.energy())
        dr = Tlv.DeltaR(electronTlv)
        if dr < 0.15:
            flag = 0
            break
#    print flag
    return flag



def drjet(Tlv,jetlist = [], *args):
    flag = 1
    for jet in jetlist:
        if jet.pt() < 10:continue
        jetTlv = TLorentzVector()
        jetTlv.SetPxPyPzE(jet.px(),jet.py(),jet.pz(),jet.energy())
        dr = Tlv.DeltaR(jetTlv)
        if dr < 0.5:
            flag = 0
            break
#    print flag
    return flag

def reliso(trk,trklist =[], *args):
    trkTlv = TLorentzVector()
    trkTlv.SetPxPyPzE(trk.px(), trk.py(), trk.pz(), trk.pt())
    trackiso = 0
    sumPt = 0
    for track in trklist:
        trackTlv = TLorentzVector()
        trackTlv.SetPxPyPzE(track.px(), track.py(), track.pz(), track.pt())
        if trackTlv.DeltaR(trkTlv) < 0.3 : sumPt = sumPt + track.pt()
    trackiso = (sumPt - (trk.pt()))/trk.pt()
    return trackiso

def miniso(trk, trklist =[], *args):

    trkTlv = TLorentzVector()
    trkTlv.SetPxPyPzE(trk.px(), trk.py(), trk.pz(), trk.pt())
    trackiso = 0
    sumPt = 0
    r = 0.3
    if trk.pt() <50: r = 0.2
    elif trk.pt() >=50 and trk.pt() < 200: r = 10/trk.pt()
    elif trk.pt() >=200 : r = 0.05
#    print r
    for track in trklist:
        trackTlv = TLorentzVector()
        trackTlv.SetPxPyPzE(track.px(), track.py(), track.pz(), track.pt())

        if trackTlv.DeltaR(trkTlv) < r : sumPt = sumPt + track.pt()
    trackiso = (sumPt - (trk.pt()))/trk.pt()
    return trackiso


main()
