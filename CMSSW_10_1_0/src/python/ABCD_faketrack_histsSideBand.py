from ROOT import *
import sys
import numpy as np
from DataFormats.FWLite import Events, Handle
import scipy.constants as scc
import math
from glob import glob
from FWCore.ParameterSet.VarParsing import VarParsing
#from utilsII import *
from utilitiesII import *
gROOT.SetBatch()
gROOT.SetStyle('Plain')

########################################
#Differences and similarity in Side Band and Main Band script:
#1: No Z -> mu mu event selection in main band so , lepton veto applied in Main band
#2:Side Band script can be run on MC and DATA both to get HIsts for Alpha factors.
#3: Main band script makes sence to get Alpha factor from MC closure (with Genmatching of Fakes), Can be used get CR in Main Band (Kind of half Work
#  done for Fake BKG estimatino script)
# kind of a closure test, Seperate script for Complete closure of Fake Bkg and sililar script for prediction.
#4:: A crappy disappearing track selected in CR in both script
#Assumption (almost true): Only Fakes enter the CR of Side and Main band. Only fakes enter in SR of Main Band
########################################



try: inputFileNames = sys.argv[1]
except:
    inputFileNames = "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1_391_RA2AnalysisTree.root"
inputFiles = glob(inputFileNames)
x_ = len(inputFiles)
print 'going to analyze events in', inputFileNames

if 'Run20' in inputFileNames: isdata = True  # for DATA
else: isdata = False
verbose = False
if not isdata:
    if 'TTJets_TuneCUET' in inputFileNames:  madranges = [(0,600),(800,1200)]
    elif 'DYJetsToLL_M-50_TuneCUETP8M1' in inputFileNames: madranges = [(0, 100)]
    elif 'TTJets_HT' in inputFileNames: madranges = [(600,inf)]
    elif 'WJetsToLNu_TuneCUET' in inputFileNames: madranges = [(0, 100), (600,800)]
    elif 'WJetsToLNu_HT' in inputFileNames: madranges = [(100, inf)]
    elif 'Summer16.DYJetsToLL_M-50_HT' in inputFileNames: madranges = [(0, inf)]
    else: madranges = [(0, inf)]

if not isdata: print 'Will Run on print madranges:' ,  madranges
#trigger names
ElectronTriggers = [14, 15, 16, 17, 18, 19, 20, 21]
MuonTriggers = [24,25,26,27,28,30,31,32]

def TriggerResult(trigger):
    for i, index in enumerate(trigger):
        if c.TriggerPass[index] ==1: return True
    return False

fMask = TFile('/nfs/dust/cms/user/singha/LLCh/BACKGROUNDIII/CMSSW_10_1_0/src/usefulfiles/Mask6mar.root')
if isdata : hMask = fMask.Get('hEtaVsPhiDT_maskData-2016Data-2016')
#if isdata : hMask = fMask.Get('hEtaVsPhiDT_maskRun2016')
else : hMask = ''

c = TChain("TreeMaker2/PreSelection")

pdgIDs = [0, 11, 13, 15, 100, 'other', 'all']
track_category = ['inclusive','small','medium','long']
trkVars = ['Pt', 'eta','dxy','dz','sumNpt','rsumNpt','sumCpt','rsumCpt','calodep','rIso','ohits','mihits','length','pterr']
eventVars = ['Pt','MET','HT','MHT','dPhiMin','dPhiMax','dPhimaxjets','dPhijet1','dPhi','mhtdPhi','R','mhtR','nJets','nbJets','nDtrks','nVtx']
Dvars = ['PtVSdPhi', 'METVSdPhi','PtVSR', 'METVSR', 'RVSdPhi']
regionkeys = ['SBSRnum', 'SBCRden']
eventVarsCuts = [200, 250,0,0,1,0]
dBkgComposition2DHist = {}
dBkgCompositionHist = {}
hHt                          = TH1F("hHt","HT for number of events", 150,0,2500)
hHtWeighted                  = TH1F("hHtWeighted","HT for number of events", 250,0,5000)
hbkgID                       = TH1F("hbkgID", "background pdgID", 50, -25, 25)
hInvMass                     = TH1F("hInvMass", "Invariant Mass #mu #mu", 60, 60, 120)
hInvMassAccept               = TH1F("hInvMassAccept", "InvMass of Fake trk events", 60, 60, 120)
for ipdg, pdg in enumerate(pdgIDs):
    for icategory, category in enumerate(track_category):
        for iregion, regionkey in enumerate(regionkeys):
            for ivar, var in enumerate(eventVars):
                newHistKey = 'Bkg'+category+'_'+var+'_'+regionkey+'_'+str(pdg)
                print newHistKey
                if '_Pt_' in newHistKey: dBkgCompositionHist[newHistKey] = TH1F(newHistKey, newHistKey, len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'))
                if '_MHT_' in newHistKey: dBkgCompositionHist[newHistKey] = TH1F(newHistKey, newHistKey, len(MHTBinEdges)-1,np.asarray(MHTBinEdges, 'd'))
                if '_MET_' in newHistKey: dBkgCompositionHist[newHistKey] = TH1F(newHistKey, newHistKey, len(METBinEdges)-1,np.asarray(METBinEdges, 'd'))
                if '_HT_' in newHistKey: dBkgCompositionHist[newHistKey] = TH1F(newHistKey, newHistKey, len(HTBinEdges)-1,np.asarray(HTBinEdges, 'd'))
                if '_nJets_' in newHistKey: dBkgCompositionHist[newHistKey] = TH1F(newHistKey, newHistKey, len(JetBinEdges)-1,np.asarray(JetBinEdges, 'd'))
                if '_nbJets_' in newHistKey: dBkgCompositionHist[newHistKey] = TH1F(newHistKey, newHistKey, len(JetBinEdges)-1,np.asarray(JetBinEdges, 'd'))
                if '_dPhi_' in newHistKey: dBkgCompositionHist[newHistKey] = TH1F(newHistKey, newHistKey, 40, -0.001, 3.2)
                if '_mhtdPhi_' in newHistKey: dBkgCompositionHist[newHistKey] = TH1F(newHistKey, newHistKey, 40, -0.001, 3.2)
                if '_dPhiMin_' in newHistKey: dBkgCompositionHist[newHistKey] = TH1F(newHistKey, newHistKey, 40, -0.001, 3.2)
                if '_dPhiMax_' in newHistKey: dBkgCompositionHist[newHistKey] = TH1F(newHistKey, newHistKey, 40, -0.001, 3.2)
                if '_dPhimaxjets_' in newHistKey: dBkgCompositionHist[newHistKey] = TH1F(newHistKey, newHistKey, 40, -0.001, 3.2)
                if '_dPhijet1_' in newHistKey: dBkgCompositionHist[newHistKey] = TH1F(newHistKey, newHistKey, 40, -0.001, 3.2)
                if '_R_' in newHistKey: dBkgCompositionHist[newHistKey] = TH1F(newHistKey, newHistKey, 20, -0.001, 3)
                if '_mhtR_' in newHistKey: dBkgCompositionHist[newHistKey] = TH1F(newHistKey, newHistKey, 20, -0.001, 3)
                if '_nDtrks_' in newHistKey: dBkgCompositionHist[newHistKey] = TH1F(newHistKey, newHistKey, 4, 0, 4)
                if '_nVtx_' in newHistKey: dBkgCompositionHist[newHistKey] = TH1F(newHistKey, newHistKey, 20, 0, 80)
                histoStyler(dBkgCompositionHist[newHistKey], 1)

            for iDvar, Dvar in enumerate(Dvars):
                new2DHistKey = 'Bkg'+category+Dvar+regionkey+'_'+str(pdg)
                if 'PtVSdPhi' in new2DHistKey: dBkgComposition2DHist[new2DHistKey] = TH2D(new2DHistKey,new2DHistKey , len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'), 40, -0.001, 3.2)
                if 'METVSdPhi' in new2DHistKey: dBkgComposition2DHist[new2DHistKey] = TH2D(new2DHistKey,new2DHistKey , len(METBinEdges)-1,np.asarray(METBinEdges, 'd'), 40, -0.001, 3.2)
                if 'PtVSR' in new2DHistKey: dBkgComposition2DHist[new2DHistKey] = TH2D(new2DHistKey,new2DHistKey , len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'), 20, -0.001, 3)
                if 'METVSR' in new2DHistKey: dBkgComposition2DHist[new2DHistKey] = TH2D(new2DHistKey,new2DHistKey , len(METBinEdges)-1,np.asarray(METBinEdges, 'd'), 20, -0.001, 3)
                if 'RVSdPhi' in new2DHistKey: dBkgComposition2DHist[new2DHistKey] = TH2D(new2DHistKey,new2DHistKey ,  20, -0.001, 3, 40, -0.001, 3.2)

for f in inputFiles:
    print 'adding file:', f
    c.Add(f)
nentries = c.GetEntries()
c.Show(0)
print nentries, ' events to be analyzed'
verbosity = 10000
identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('Summer16.','').replace('RA2AnalysisTree','')
identifier+='nFiles'+str(len(inputFiles))

Pt_threshold = 30
def main():
                
#eventPreselection
#        if not (c.HT > 250 and c.MHT > 200 and c.MET > 130 ):continue # uncomment for main band
    for ientry in range(nentries):
        if verbose:
            if not ientry in [670]: continue
        if ientry%verbosity==0: print 'now processing event number', ientry, 'of', nentries
        c.GetEntry(ientry)
        if isdata: weight = 1
        else: weight = c.CrossSection
        fillth1(hHt, c.HT, 1)
        fillth1(hHtWeighted, c.HT, weight)
        if not isdata:
            if weight ==1: isValidHtRange = True
            else: isValidHtRange = False
            for madrange in madranges:
                if (c.madHT>madrange[0] and c.madHT<madrange[1]):
                    isValidHtRange = True
                    break
            if not isValidHtRange: continue

        if not passesUniversalSelection(c): continue
        if c.BTags > 0: continue
        if isdata:
            if TriggerResult(MuonTriggers) == False: continue
        muon_ID1 = -1
        muon_ID2 = -1
        muTlvsum = TLorentzVector()
        muTlvsum.SetPxPyPzE(0, 0, 0, 0)
        ZToMuMuevent = False
        MuMuIM = 0
        dIM = 999
        for imu1, mu1 in enumerate(c.Muons):
            if mu1.Eta() > 2.4:continue
            if mu1.Pt() < 30:continue
            if c.Muons_tightID[imu1] == 0: continue
            for imu2, mu2 in enumerate(c.Muons):
                if not (c.Muons_charge[imu1] + c.Muons_charge[imu2] == 0) : continue
                if mu2.Eta() > 2.4:continue
                if mu2.Pt() < 30:continue
                if c.Muons_tightID[imu2] ==0: continue
                muTlvsum = mu1 + mu2
                IM = muTlvsum.M()
                if abs(IM-91) < dIM:
                    muon_ID1 = imu1
                    muon_ID2 = imu2
                    MuMuIM = IM
                    dIM= abs(IM-91)
        if abs(MuMuIM-91) < 10:
            ZToMuMuevent = True
        if MuMuIM > 0:
            fillth1(hInvMass, MuMuIM, weight)
        #    print ZToMuMuevent, 'Mu Mu invariant mass is :', MuMuIM
        if ZToMuMuevent == False: continue                          # comment for main band
#        print ZToMuMuevent, 'Mu Mu invariant mass is :', MuMuIM
#        if leptonVeto(muon_ID1, muon_ID2) == False: continue # comment for main band Be carefull when apply Lepton Veto  
        track_type = 'Nil'
        region = 'Nil'
        orthogonalCheck = 0
        nDtrk = 0
        basicTracks = []
        disappearingTracks = [] # fill as trk, trkID, track length
        gen_pdgID = -99 # gen Id of Bkg track        
        for itrack, track in enumerate(c.tracks):
            length = 0
            S = 0
            M = 0
            L = 0
            if not (track.Pt() > 20): continue
            if (abs(track.Eta()) > 1.4442 and abs(track.Eta()) < 1.566): continue
            if abs(track.Eta()) > 2.4 : continue
            if c.tracks_pixelLayersWithMeasurement[itrack] == c.tracks_trackerLayersWithMeasurement[itrack]:
                S = 1
                length = 1
            if c.tracks_trackerLayersWithMeasurement[itrack] < 7 and c.tracks_pixelLayersWithMeasurement[itrack] < c.tracks_trackerLayersWithMeasurement[itrack] :
                M = 1
                length = 3
            if c.tracks_trackerLayersWithMeasurement[itrack] > 6 and c.tracks_pixelLayersWithMeasurement[itrack] < c.tracks_trackerLayersWithMeasurement[itrack]:
                L = 1
                length = 5
            if not isNminusOneBaselineTrack(track, itrack, c, hMask): continue  # removed the dxy cut : it is used later to define the track in CR or SR
            if not track.Pt() < 9999: continue
            basicTracks.append([track,c.tracks_charge[itrack], itrack])
            if not track.Pt() > Pt_threshold : continue
            if not isDisappearingTrack_(track, itrack, c): continue  #in principle it is N minus one disappearing track
            drlep = 99
            passeslep = True  # checking lepton overlap
            for ilep, lep in enumerate(list(c.Electrons)+list(c.Muons) +list(c.TAPPionTracks)):
                drlep = min(drlep, lep.DeltaR(track))
                if drlep<0.01:
                    passeslep = False
                    break
            if not passeslep: continue
            if abs(c.tracks_dxyVtx[itrack]) < 0.01: 
                region = 'SBSRnum'
                orthogonalCheck = orthogonalCheck + 1
            if ((abs(c.tracks_dxyVtx[itrack]) > 0.02) and (abs(c.tracks_dxyVtx[itrack]) < 0.1)) : 
                region = 'SBCRden'
                orthogonalCheck= orthogonalCheck + 1
            if region == 'Nil': continue     # disappearing track definition ends here, track end up either in CR or SR 
            
            if orthogonalCheck == 2:
                print 'event is in SR and CR both'
#                continue
            disappearingTracks.append([track,itrack])
            if len(disappearingTracks) == 1: 
                if isdata :gen_pdgID = 0     # Assume the track to be a fake track checked in MC
                else: gen_pdgID = getGenID(track)
                if length == 1: track_type = 'small'
                if length == 3: track_type = 'medium'
                if length == 5: track_type = 'long'
            else: gen_pdgID = 100  # will show if there are more than one DispTrack
        
        trkTlvsum = TLorentzVector()
        trkTlvsum.SetPxPyPzE(0, 0, 0, 0)
        if len(disappearingTracks) > 0:
            fillth1(hInvMassAccept, MuMuIM, weight)
            nDtrk = len(disappearingTracks)
            for idtrk, dtrk in enumerate(disappearingTracks):
                trkTlvsum = trkTlvsum + dtrk[0]

            Njets  = nJets(disappearingTracks)
            MHT = getMht(disappearingTracks)
            HT = getHt(disappearingTracks)
            NBjets = nbJets(disappearingTracks)
            deltaPhi    = math.acos(math.cos((c.METPhi-trkTlvsum.Phi())))
            mhtdeltaPhi = math.acos(math.cos((MHT.Phi()-trkTlvsum.Phi())))
            DPt     = 2*(abs(c.MET-trkTlvsum.Pt())/(c.MET+trkTlvsum.Pt()))
            mhtDPt  = 2*(abs(MHT.Pt()-trkTlvsum.Pt())/(MHT.Pt()+trkTlvsum.Pt()))
            mindphi = minDeltaPhi(c.METPhi)
            maxdphi = maxDeltaPhi(c.METPhi)
            maxdphijets = DeltaPhiJets()
            dphijet1 = DeltaPhiJet1(c.METPhi)

            if not deltaPhi > 0.5: continue
# eventVars = ['Pt','MET','HT','MHT','dPhiMin','dPhiMax','dPhimaxjets','dPhijet1','dPhi','mhtdPhi','R','mhtR','nJets','nbJets','nDtrks']
            fveventVar = [trkTlvsum.Pt(), c.MET, HT, MHT, mindphi, maxdphi, maxdphijets, dphijet1, deltaPhi, mhtdeltaPhi, DPt, mhtDPt, Njets, NBjets, nDtrk, c.nAllVertices]
# Dvars = ['PtVSdPhi', 'METVSdPhi','PtVSR', 'METVSR', 'RVSdPhi']
            fvDvar = [[trkTlvsum.Pt(),deltaPhi], [c.MET, deltaPhi], [trkTlvsum.Pt(), DPt], [c.MET , DPt], [DPt, deltaPhi]]
            print region
            fillBkgCompositionHist(fveventVar, fvDvar, gen_pdgID, weight, track_type, region)
#        else: continue

    fnew = TFile('SB_FakeHists_'+identifier+'.root','recreate')
    hHt.Write()
    hHtWeighted.Write()
    hbkgID.Write()
    hInvMass.Write()
    hInvMassAccept.Write()
    for histkey in dBkgCompositionHist: dBkgCompositionHist[histkey].Write()
    for Dhistkey in dBkgComposition2DHist: dBkgComposition2DHist[Dhistkey].Write()
    print "just created" , fnew.GetName()
    fnew.Close()

def getGenID(track):
    drsmall = 0.2
    gen_id = 0
    for igen, gen in enumerate(c.GenParticles):
        if not ((c.GenParticles_Status[igen] == 1) or (abs(c.GenParticles_PdgId[igen]) == 15)) : continue
        if gen.Pt() < 15:continue
        dr = gen.DeltaR(track)
        if dr < drsmall:
            drsmall = dr
            gen_id  = abs(c.GenParticles_PdgId[igen]) 
    if drsmall < 0.01: return gen_id
    else : return 0

def minDeltaPhi(METPhi):  #between MET and any of Jets
    deltaPhi = 10
    for ijet, jet in enumerate(c.Jets):
        if not (abs(jet.Eta() < 5.0) and jet.Pt() > 30): continue
        if not c.Jets_ID[ijet]: continue
        deltaPhi_temp = math.acos(math.cos((METPhi-jet.Phi())))
        if deltaPhi > deltaPhi_temp: deltaPhi = deltaPhi_temp
    return deltaPhi

def maxDeltaPhi(METPhi): # between MET and any of jets
    deltaPhi = -10
    for ijet, jet in enumerate(c.Jets):
        if not (abs(jet.Eta() < 5.0) and jet.Pt() > 30): continue
        if not c.Jets_ID[ijet]: continue
        deltaPhi_temp = math.acos(math.cos((METPhi-jet.Phi())))
        if deltaPhi < deltaPhi_temp: deltaPhi = deltaPhi_temp
    return deltaPhi

def DeltaPhiJets():
    deltaPhi = -10
    for ijet1, jet1 in enumerate(c.Jets):
        if not (abs(jet1.Eta() < 5.0) and jet1.Pt() > 30): continue
        if not c.Jets_ID[ijet1]: continue
        for ijet2, jet2 in enumerate(c.Jets):
            if ijet1 == ijet2: continue
            if not c.Jets_ID[ijet2]: continue
            deltaPhi_temp = math.acos(math.cos((jet1.Phi()-jet2.Phi())))
            if deltaPhi < deltaPhi_temp: deltaPhi = deltaPhi_temp
    return deltaPhi

    
def DeltaPhiJet1(METPhi):
    jet_leading = TLorentzVector()
    jet_leading.SetPtEtaPhiE(0,0,0,0)
    Pt_leading = 0
    deltaPhi = 0
    for ijet, jet in enumerate(c.Jets):
        if not (abs(jet.Eta() < 5.0) and jet.Pt() > 30): continue
        if not c.Jets_ID[ijet]: continue
        if Pt_leading < jet.Pt():  
            Pt_leading = jet.Pt()
            jet_leading = jet
    if Pt_leading > 0 : deltaPhi = math.acos(math.cos((METPhi-jet.Phi())))
    return deltaPhi




def nJets(tracklist):
    njets = 0
    for ijet, jet in enumerate(c.Jets):
        omitJet= False
        for itrack, track in enumerate(tracklist):
            if not jet.DeltaR(track[0])>0.04: omitJet= True
        if omitJet: continue        
        if not (abs(jet.Eta() < 2.4) and jet.Pt() > 30): continue
        if not c.Jets_ID[ijet]: continue
        njets = njets + 1
    return njets

def getHt(tracklist):
    adjustedHt = 0
    for ijet, jet in enumerate(c.Jets):
        omitJet= False
        for itrack, track in enumerate(tracklist):
            if not jet.DeltaR(track[0])>0.04: omitJet= True
        if omitJet: continue
        if not jet.Pt()>30: continue
        if not abs(jet.Eta())<2.4: continue
        if not c.Jets_ID[ijet]: continue
        adjustedHt+=jet.Pt()
    return adjustedHt

def getMht(tracklist):
    adjustedMht = TLorentzVector()
    adjustedMht.SetPxPyPzE(0,0,0,0)
    for ijet, jet in enumerate(c.Jets):
        omitJet= False
        for itrack, track in enumerate(tracklist):
            if not jet.DeltaR(track[0])>0.04: omitJet= True
        if omitJet: continue
        if not jet.Pt()>30: continue
        if not abs(jet.Eta())<5.0: continue
        if not c.Jets_ID[ijet]: continue
        adjustedMht-=jet
    return adjustedMht

def nbJets(tracklist):
    nbjets = 0
    csv_b = 0.8484
    for ijet, jet in enumerate(c.Jets):
        omitJet= False
        for itrack, track in enumerate(tracklist):
            if not jet.DeltaR(track[0])>0.04: omitJet= True
        if omitJet: continue
        if not c.Jets_ID[ijet]: continue
        if not (abs(jet.Eta() < 2.4) and jet.Pt() > 30): continue
        if not  c.Jets_bDiscriminatorCSV[ijet]>csv_b: continue
        nbjets =nbjets +1
    return nbjets

def fillBkgCompositionHist(Eventfv, Event2Dfv, pdgId, w, trk_type, regionkey):
    if pdgId in pdgIDs: pdgId = str(pdgId)
    else : pdgId = 'other'

    for ivar, var in enumerate(eventVars):
        
        histkey = 'Bkg'+trk_type+'_'+var+'_'+regionkey+'_'+pdgId
        fillth1(dBkgCompositionHist[histkey], Eventfv[ivar], w) 
        histkey_allParticles = 'Bkg'+trk_type+'_'+var+'_'+regionkey+'_all'
        fillth1(dBkgCompositionHist[histkey_allParticles], Eventfv[ivar], w)
#now fill the inclusive tracks
        histkey_inclusive = 'Bkg'+'inclusive'+'_'+var+'_'+regionkey+'_'+pdgId
        fillth1(dBkgCompositionHist[histkey_inclusive], Eventfv[ivar], w)
        histkey_inclusive_allParticles = 'Bkg'+'inclusive'+'_'+var+'_'+regionkey+'_all'
        fillth1(dBkgCompositionHist[histkey_inclusive_allParticles], Eventfv[ivar], w)

    for iDvar, Dvar in enumerate(Dvars):

        Dhistkey = 'Bkg'+trk_type+Dvar+regionkey+'_'+pdgId
        fillth2(dBkgComposition2DHist[Dhistkey], Event2Dfv[iDvar][0],Event2Dfv[iDvar][1], w)
        Dhistkey_allParticles = 'Bkg'+trk_type+Dvar+regionkey+'_all'
        fillth2(dBkgComposition2DHist[Dhistkey_allParticles], Event2Dfv[iDvar][0],Event2Dfv[iDvar][1], w)
#now fill the inclusive tracks 
        Dhistkey_inclusive = 'Bkg'+'inclusive'+Dvar+regionkey+'_'+pdgId
        fillth2(dBkgComposition2DHist[Dhistkey_inclusive], Event2Dfv[iDvar][0],Event2Dfv[iDvar][1], w)
        Dhistkey_inclusive_allParticles = 'Bkg'+'inclusive'+Dvar+regionkey+'_all'
        fillth2(dBkgComposition2DHist[Dhistkey_inclusive_allParticles], Event2Dfv[iDvar][0],Event2Dfv[iDvar][1], w)

    return True


main()


