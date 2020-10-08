from ROOT import *
import sys
import numpy as np
from DataFormats.FWLite import Events, Handle
import scipy.constants as scc
import math
from glob import glob
from FWCore.ParameterSet.VarParsing import VarParsing
from random import shuffle
from utilitiesII import *

gROOT.SetBatch()
gROOT.SetStyle('Plain')


hHTnum                          = TH1F("hHTnum","HT for number of events", 150,40,2500)
histoStyler(hHTnum,1)

dEletrkResponseHist = {}
for iPtBin, PtBin in enumerate(PtBinEdgesForSmearing[:-1]):
        for iEtaBin, EtaBin in enumerate(EtaBinEdgesForSmearing[:-1]):
                newHistKey = ((EtaBin,EtaBinEdgesForSmearing[iEtaBin + 1]),(PtBin,PtBinEdgesForSmearing[iPtBin + 1]))
                dEletrkResponseHist[newHistKey] = TH1D("heletrkresp"+str(newHistKey),"heletrkresp"+str(newHistKey), 200,-2,2)
                histoStyler(dEletrkResponseHist[newHistKey], 1)

dMutrkResponseHist = {}
for iPtBin, PtBin in enumerate(PtBinEdgesForSmearing[:-1]):
        for iEtaBin, EtaBin in enumerate(EtaBinEdgesForSmearing[:-1]):
                newHistKey = ((EtaBin,EtaBinEdgesForSmearing[iEtaBin + 1]),(PtBin,PtBinEdgesForSmearing[iPtBin + 1]))
                dMutrkResponseHist[newHistKey] = TH1D("hmutrkresp"+str(newHistKey),"hmutrkresp"+str(newHistKey), 200,-2,2)
                histoStyler(dMutrkResponseHist[newHistKey], 1)

dEleResponseHist = {}
for iPtBin, PtBin in enumerate(PtBinEdgesForSmearing[:-1]):
        for iEtaBin, EtaBin in enumerate(EtaBinEdgesForSmearing[:-1]):
                newHistKey = ((EtaBin,EtaBinEdgesForSmearing[iEtaBin + 1]),(PtBin,PtBinEdgesForSmearing[iPtBin + 1]))
                dEleResponseHist[newHistKey] = TH1D("heleresp"+str(newHistKey),"heleresp"+str(newHistKey), 200,-2,2)
                histoStyler(dEleResponseHist[newHistKey], 1)

dMuResponseHist = {}
for iPtBin, PtBin in enumerate(PtBinEdgesForSmearing[:-1]):
        for iEtaBin, EtaBin in enumerate(EtaBinEdgesForSmearing[:-1]):
                newHistKey = ((EtaBin,EtaBinEdgesForSmearing[iEtaBin + 1]),(PtBin,PtBinEdgesForSmearing[iPtBin + 1]))
                dMuResponseHist[newHistKey] = TH1D("hmuresp"+str(newHistKey),"hmuresp"+str(newHistKey), 200,-2,2)
                histoStyler(dMuResponseHist[newHistKey], 1)


####
#Input File    

try: inputFileNames = sys.argv[1]
except:
	inputFileNames = "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2_285_RA2AnalysisTree.root"

inputFiles = glob(inputFileNames)

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
        hHTnum.Fill(c.madHT)
#	if not (c.HT > 100): continue
#        if not(c.NJets > 1 and c.NJets < 4): continue

	if not c.CaloMET/c.MET<5.0: continue
	genels = []
	genmus = []

	for igp, gp in enumerate(c.GenParticles):
		if not gp.Pt()>5: continue
		if not (abs(c.GenParticles_PdgId[igp])==11 or abs(c.GenParticles_PdgId[igp])==13) : continue
		if not c.GenParticles_Status[igp]==1 : continue
		if not abs(gp.Eta())<2.4: continue
		if not (abs(gp.Eta())<1.445 or abs(gp.Eta())>1.56): continue
		if abs(c.GenParticles_PdgId[igp])==11: genels.append([gp,igp])
		if abs(c.GenParticles_PdgId[igp])==13: genmus.append([gp,igp])

	basicTracks = []
	disappearingTracks = []
	for itrack, track in enumerate(c.tracks):
		if not track.Pt() > 20 : continue
		if not abs(track.Eta()) < 2.4: continue
		if not (abs(track.Eta()) > 1.566 or abs(track.Eta()) < 1.4442): continue
		if not isBaselineTrack(track, itrack, c): continue
		if not track.Pt()<9999: continue
		basicTracks.append([track,c.tracks_charge[itrack], itrack])
		if not track.Pt()<9999: continue
		if not isDisappearingTrack_(track, itrack, c): continue

		drlep = 99
		passeslep = True  # checking lepton overlap                                                                 
		for ilep, lep in enumerate(list(c.Electrons)+list(c.Muons)):
			drlep = min(drlep, lep.DeltaR(track))
			if drlep<0.01:
				passeslep = False
				break
		if not passeslep: continue
		disappearingTracks.append([track,c.tracks_charge[itrack]])


	Electrons = []
	for ilep, lep in enumerate(c.Electrons):
		if not lep.Pt()>5: continue
		if (abs(lep.Eta()) < 1.566 and abs(lep.Eta()) > 1.4442): continue
		if not abs(lep.Eta())<2.4: continue
		if not c.Electrons_passIso[ilep]: continue
		if not c.Electrons_mediumID[ilep]: continue                                                                
		matchedTrack = TLorentzVector()
		drmin = 9999
		for trk in basicTracks:
			if not c.tracks_nMissingOuterHits[trk[2]]==0: continue
			drTrk = trk[0].DeltaR(lep)
			if drTrk<drmin:
				drmin = drTrk
				matchedTrack = trk[0]
				if drTrk<0.01: break
		if not drmin<0.01: continue
		Electrons.append([lep, matchedTrack])

	Muons = []
	for ilep, lep in enumerate(c.Muons):
		if not lep.Pt()>5: continue
		if (abs(lep.Eta()) < 1.566 and abs(lep.Eta()) > 1.4442): continue
		if not abs(lep.Eta())<2.4: continue
		if not c.Muons_passIso[ilep]: continue
		matchedTrack = TLorentzVector()
		drmin = 9999
		for trk in basicTracks:
			if not c.tracks_nMissingOuterHits[trk[2]]==0: continue
			drTrk = trk[0].DeltaR(lep)
			if drTrk<drmin:
				drmin = drTrk
				matchedTrack = trk[0]
				if drTrk<0.01: break
		if not drmin<0.01: continue
		Muons.append([lep,matchedTrack])


        
        for igen, genlep in enumerate(genels):
		for ie, lep in enumerate(Electrons):
			dr = genlep[0].DeltaR(lep[1])
			if not dr < 0.02: continue
			for histkey in  dEleResponseHist:
				if abs(lep[1].Eta()) > histkey[0][0] and abs(lep[1].Eta()) < histkey[0][1] and genlep[0].Pt() > histkey[1][0] and min(genlep[0].Pt(),309.999) < histkey[1][1]: fillth1(dEleResponseHist[histkey],math.log10(lep[1].Pt()/genlep[0].Pt()),weight)

		for idtrk, dtrk in enumerate(disappearingTracks):
			dr = genlep[0].DeltaR(dtrk[0])
			if not dr < 0.02: continue
			for histkey in  dEletrkResponseHist:
                                if abs(dtrk[0].Eta()) > histkey[0][0] and abs(dtrk[0].Eta()) < histkey[0][1] and genlep[0].Pt() > histkey[1][0] and min(genlep[0].Pt(),309.999) < histkey[1][1]: fillth1(dEletrkResponseHist[histkey],math.log10(dtrk[0].Pt()/genlep[0].Pt()),weight)


	for igen, genlep in enumerate(genmus):
                for ie, lep in enumerate(Muons):
			dr = genlep[0].DeltaR(lep[1])
			if not dr < 0.02: continue
                        for histkey in  dMuResponseHist:
                                if abs(lep[1].Eta()) > histkey[0][0] and abs(lep[1].Eta()) < histkey[0][1] and genlep[0].Pt() > histkey[1][0] and min(genlep[0].Pt(),309.999) < histkey[1][1]: fillth1(dMuResponseHist[histkey],math.log10(lep[1].Pt()/genlep[0].Pt()),weight)

		for idtrk, dtrk in enumerate(disappearingTracks):
                        dr = genlep[0].DeltaR(dtrk[0])
                        if not dr < 0.02: continue
                        for histkey in  dMutrkResponseHist:
                                if abs(dtrk[0].Eta()) > histkey[0][0] and abs(dtrk[0].Eta()) < histkey[0][1] and genlep[0].Pt() > histkey[1][0] and min(genlep[0].Pt(),309.999) < histkey[1][1]: fillth1(dMutrkResponseHist[histkey],math.log10(dtrk[0].Pt()/genlep[0].Pt()),weight)



    ftem = TFile('BinnedTemplate_Hists'+identifier+'.root','recreate')
    ftem.cd()

    for histkey in  dEleResponseHist: dEleResponseHist[histkey].Write()
    for histkey in  dMuResponseHist: dMuResponseHist[histkey].Write()
    for histkey in  dEletrkResponseHist: dEletrkResponseHist[histkey].Write()
    for histkey in  dMutrkResponseHist: dMutrkResponseHist[histkey].Write()

    ftem.Close()
    print "file:", ftem, "created."
main()
