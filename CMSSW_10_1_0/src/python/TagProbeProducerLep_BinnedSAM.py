from ROOT import *
import sys
import numpy as np
import scipy.constants as scc
import math
from glob import glob
from random import shuffle
from utils import *
import random

options = VarParsing ('python')
options.parseArguments()

gROOT.SetBatch()
gROOT.SetStyle('Plain')
inputFiles = options.inputFiles

try: inputFiles = sys.argv[1]
except: inputFiles = '/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1_391_RA2AnalysisTree.root'
c = TChain("TreeMaker2/PreSelection")
globbedFiles = glob(inputFiles)
for file_ in globbedFiles: c.Add(file_)
nentries = c.GetEntries()

fname = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDII/CMSSW_8_0_20/src/MCTemplatesBinned/BinnedTemplates.root'
fSmear  = TFile(fname)

dResponseHist = {}
for iPtBin, PtBin in enumerate(PtBinEdges[:-1]):
        for iEtaBin, EtaBin in enumerate(EtaBinEdges[:-1]):
                newHistKey = ((EtaBin,EtaBinEdges[iEtaBin + 1]),(PtBin,PtBinEdges[iPtBin + 1]))
                dResponseHist[newHistKey] = fSmear.Get("htrkresp"+str(newHistKey))

def main():

	verbosity = 1000
	identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('Summer16.','').replace('RA2AnalysisTree','')
	identifier+='nFiles'+str(len(inputFiles))

	hHTnum                = TH1D("hHTnum","HT for number of events", 150,40,2500)
	histoStyler(hHTnum,1)
	hne                  = TH1F("hne", "number of electrons", 4, 0, 4)
	histoStyler(hne,1)	
	hIMcheck                  = TH1D("hIMcheck"  , "IM  ", 60, 20, 180)
	histoStyler(hIMcheck,1)	
	hEleGenPt             = TH1D("hEleGenPt", ";m [GeV] ;pt of the gen Ele;;", len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'))
	histoStyler(hEleGenPt,1)	
	hEleGenPtRECOeff      = TH1D("hEleGenPtRECOeff", ";m [GeV] ;pt of the RECO Ele;;", len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'))
	histoStyler(hEleGenPtRECOeff,1)
	hEleGenPtDTeff        = TH1D("hEleGenPtDTeff", "pt of the DT Ele", len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'))
	histoStyler(hEleGenPtDTeff,1)
	hEleGenPtSDTeff        = TH1D("hEleGenPtSDTeff", "pt of the SDT Ele", len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'))
	histoStyler(hEleGenPtSDTeff,1)
	hEleGenPtMDTeff        = TH1D("hEleGenPtMDTeff", "pt of the MDT Ele", len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'))
	histoStyler(hEleGenPtMDTeff,1)
	hEleGenPtLDTeff        = TH1D("hEleGenPtLDTeff", "pt of the LDT Ele", len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'))
	histoStyler(hEleGenPtLDTeff,1)
	hEleGenEta            = TH1D("hEleGenEta", "Eta of the gen Ele", len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
	histoStyler(hEleGenEta,1)
	hEleGenEtaRECOeff     = TH1D("hEleGenEtaRECOeff", "Eta of the gen Ele", len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
	histoStyler(hEleGenEtaRECOeff,1)
	hEleGenEtaDTeff       = TH1D("hEleGenEtaDTeff", "Eta of the reco Ele", len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
	histoStyler(hEleGenEtaDTeff,1)
	hEleGenEtaSDTeff       = TH1D("hEleGenEtaSDTeff", "Eta of the SDT", len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
	histoStyler(hEleGenEtaSDTeff,1)
	hEleGenEtaMDTeff       = TH1D("hEleGenEtaMDTeff", "Eta of the MDT", len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
	histoStyler(hEleGenEtaMDTeff,1)
	hEleGenEtaLDTeff       = TH1D("hEleGenEtaLDTeff", "Eta of the LDT", len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
	histoStyler(hEleGenEtaLDTeff,1)
	hEleProbePt           = TH1D("hEleProbePt", "pt of the EleProbes", len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'))
	hEleProbePtDTeff      = TH1D("hEleProbePtDTeff", "pt of the EleProbes", len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'))
	hEleProbePtSDTeff      = TH1D("hEleProbePtSDTeff", "pt of the EleProbes", len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'))
	hEleProbePtMDTeff      = TH1D("hEleProbePtMDTeff", "pt of the EleProbes", len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'))
	hEleProbePtLDTeff      = TH1D("hEleProbePtLDTeff", "pt of the EleProbes", len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'))
	hEleProbePtRECOeff    = TH1D("hEleProbePtRECOeff", "pt of the EleProbes", len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'))
	#hEleProbePtDTmeff      = TH1D("hEleProbePtDTmeff", "pt of the EleProbes", len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'))
	histoStyler(hEleProbePt,1)
	histoStyler(hEleProbePtDTeff,1)
	histoStyler(hEleProbePtSDTeff,1)
	histoStyler(hEleProbePtMDTeff,1)
	histoStyler(hEleProbePtLDTeff,1)
	histoStyler(hEleProbePtRECOeff,1)
	hEleProbeEta          = TH1D("hEleProbeEta", "Eta of the EleProbes", len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
	hEleProbeEtaDTeff     = TH1D("hEleProbeEtaDTeff", "Eta of the EleProbes", len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
	hEleProbeEtaSDTeff     = TH1D("hEleProbeEtaSDTeff", "Eta of the EleProbes", len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
	hEleProbeEtaMDTeff     = TH1D("hEleProbeEtaMDTeff", "Eta of the EleProbes", len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
	hEleProbeEtaLDTeff     = TH1D("hEleProbeEtaLDTeff", "Eta of the EleProbes", len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
	hEleProbeEtaDTmeff     = TH1D("hEleProbeEtaDTmeff", "Eta of the EleProbes", len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
	hEleProbeEtaRECOeff   = TH1D("hEleProbeEtaRECOeff", "Eta of the EleProbes", len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
	histoStyler(hEleProbeEta,1)
	histoStyler(hEleProbeEtaDTeff,1)
	histoStyler(hEleProbeEtaSDTeff,1)
	histoStyler(hEleProbeEtaMDTeff,1)
	histoStyler(hEleProbeEtaLDTeff,1)
	histoStyler(hEleProbeEtaDTmeff,1)
	histoStyler(hEleProbeEtaRECOeff,1)
	hEleTagPt             = TH1D("hEleTagPt"  , "pt of the EleTags", len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'))
	hEleTagEta            = TH1D("hEleTagEta"  , "Eta of the EleTags", len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
	histoStyler(hEleTagPt,1)
	histoStyler(hEleTagEta,1)
	hprobe                = TH1D("hprobe"  , "probe status", 2, 0, 2)
	histoStyler(hprobe,1)
	hIMmuZ                = TH1D("hIMmuZ"  , "IM z ", 60, 20, 150)
	histoStyler(hIMmuZ,1)
	hIMmuZsmear           = TH1D("hIMmuZsmear"  , "IM z smeared ", 60, 20, 150)
	histoStyler(hIMmuZsmear,1)
	hIMZ                  = TH1D("hIMZ"  , "IM z ", 40, 60, 120)
	histoStyler(hIMZ,1)

	hIMZRECOeff           = TH1D("hIMZRECOeff"  , "IM tag + RECOing probe ", 40, 60, 120)
	histoStyler(hIMZRECOeff,1)
	hIMZDTeff             = TH1D("hIMZDTeff"  , "IM tag + DTing probe ", 40, 60, 120)
	histoStyler(hIMZDTeff,1)

	hIMZDTmeff            = TH1D("hIMZDTmeff"  , "IM tag + DTing probe ", 40, 60, 120)

	histoStyler(hIMZDTmeff,1)


	hmuonresp             =TH1D("hmuonresp","muon response", 50,-3,3.2)
	histoStyler(hmuonresp,1)
	hmuonresptest         =TH1D("hmuonresptest","muon response test", 50,-3,3.2)
	histoStyler(hmuonresptest,1)

	#####
	hRelErrPtvsptMu        = TH2D("hRelErrPtvsptMu","hRelErrPtvsptMu",50, 10, 400, 20, 0 ,2)
	hRelErrPtvsptTrk       = TH2D("hRelErrPtvsptTrk","hRelErrPtvsptTrk",50, 10, 400, 20, 0 ,2)


	hEleGenEtaSDTeff       = TH1D("hEleGenEtaSDTeff", "Eta of the SDT", len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
	histoStyler(hEleGenEtaSDTeff,1)
	#####
	hGenPtvsResp        = TH2D("hGenPtvsResp","hGenPtvsResp",50, 10, 400, 20, -2 ,3)         
	histoStyler(hGenPtvsResp,1)

	hGenPtvsRespS        = TH2D("hGenPtvsRespS","hGenPtvsRespS",50, 10, 400, 20, -2 ,3)
	histoStyler(hGenPtvsRespS,1)
	hGenPtvsRespM        = TH2D("hGenPtvsRespM","hGenPtvsRespM",50, 10, 400, 20, -2 ,3)
	histoStyler(hGenPtvsRespM,1)
	hGenPtvsRespL        = TH2D("hGenPtvsRespL","hGenPtvsRespL",50, 10, 400, 20, -2 ,3)
	histoStyler(hGenPtvsRespL,1)

	hEleProbePtDTmeff      = TH1D("hEleProbePtDTmeff", "pt of the EleProbes", len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'))
	histoStyler(hEleProbePtDTmeff,1)	
	

	jentry=0
	n = 0
	f = 0
	rand = 1
	e1 = 0
	e2 = 0
	e3 = 0


		
	for ientry in range(nentries):
	
		#if not ientry==4207: continue
		if ientry%verbosity==0:
			a = 1
			print 'now processing event number', ientry
		c.GetEntry(ientry)
		#weight = (c.CrossSection*35.9)/(1*.001)
		weight = 1
		fillth1(hHTnum, c.madHT)
		flag_DT = -1
		recof = 0
		nmu = -1
		P1  =  0
		Eta1  =  0
		Phi1 = 0
		C1 = 0
		P2  =  0
		Eta2 = 0
		C2 = 0
		IM  =  0 
		dIM =  0
		dIMmax = 999
		track_id = -1
		dumTlvsum = TLorentzVector()
		dumTlvsum.SetPxPyPzE(0, 0, 0, 0)
		theTag = TLorentzVector()
		theTag.SetPxPyPzE(0, 0, 0, 0)
		tagProbeTlvSum = TLorentzVector()
		tagProbeTlvSum.SetPxPyPzE(0, 0, 0, 0)
		smearedEle = TLorentzVector()
		smearedEle.SetPtEtaPhiE(0, 0, 0, 0)
		smearedEleProbe = TLorentzVector()
		smearedEleProbe.SetPtEtaPhiE(0, 0, 0, 0)
		probeTlv = TLorentzVector()
		probeTlv.SetPxPyPzE(0, 0, 0, 0)
		dtTlvsum = TLorentzVector()
		dtTlvsum.SetPxPyPzE(0, 0, 0, 0)
		checkTlvsum = TLorentzVector()
		checkTlvsum.SetPxPyPzE(0, 0, 0, 0)
		ne = 0
		chargeCheck = 0
		muons = []
		for imu, muon in enumerate(c.Muons):
			if not muon.Pt()>10: continue
			if abs(muon.Eta()) < 1.566 and abs(muon.Eta()) > 1.4442: continue
			muons.append(muon)
		if not len(muons)==0: continue
		tightElectrons = []		
		for ie, e in enumerate(c.Electrons):
				if not (e.Pt() > 30 and bool(c.Electrons_tightID[ie])): continue
				if not (abs(e.Eta())<1.4442): continue
				if abs(e.Eta()) < 1.566 and abs(e.Eta()) > 1.4442: continue
				tightElectrons.append([e,c.Electrons_charge[ie]])
				ne = ne + 1
				if ie > 1: continue
				chargeCheck =chargeCheck + c.Electrons_charge[ie]
				checkTlvsum = checkTlvsum + e
		fillth1(hne, ne, weight)
		if (chargeCheck == 0):
				fillth1(hIMcheck, checkTlvsum.M(), weight)
		if ne == 1 : e1 +=1
		if ne == 2 : e2 +=1
		if ne >  2 : e3 +=1

		basicTracks = []
		for itrack, track in enumerate(c.tracks):
			if abs(abs(track.Eta()) < 1.566) and abs(track.Eta()) > 1.4442: continue
			if not isBaselineTrack(track, itrack): continue
			basicTracks.append(track)
			
		
		
		for igen, gen in enumerate(c.GenParticles):
			if 1 < 2:
				drsmall = .2
				drsmal  = .2
				idtrk   = -1
				idlep   = -1
				if not gen.Pt()>10: continue
				if not (abs(c.GenParticles_PdgId[igen]) == 11 and c.GenParticles_Status[igen] == 1):continue
				if not c.GenParticles_ParentId[igen] == 23: continue
				if not (abs(gen.Eta()) < 1.4442): continue
				if abs(gen.Eta()) < 1.566 and abs(gen.Eta()) > 1.4442: continue
	
				fillth1(hEleGenPt, gen.Pt(), weight)
				fillth1(hEleGenEta, abs(gen.Eta()), weight)
				for im, m in enumerate(c.Electrons):
					if not (m.Pt() > 10 and abs(m.Eta()) < 1.4442): continue
					if abs(m.Eta()) < 1.566 and abs(m.Eta()) > 1.4442: continue
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
				       # sf = getSF(abs(c.Electrons[idlep].Eta()), min(c.Electrons[idlep].Pt(),309.999))
					sf = 1 #0**(sfHist.GetRandom())
					smearedEle.SetPtEtaPhiE(sf*c.Electrons[idlep].Pt(),c.Electrons[idlep].Eta(),c.Electrons[idlep].Phi(),sf*c.Electrons[idlep].E())
					if not smearedEle.Pt()>15: continue
					fillth1(hEleGenPtRECOeff, smearedEle.Pt(), weight)
					fillth1(hEleGenEtaRECOeff, abs(c.Electrons[idlep].Eta()), weight)
					fillth1(hmuonresp, math.log10(c.Electrons[idlep].Pt()/gen.Pt()),weight)
					fillth1(hmuonresptest, math.log10(smearedEle.Pt()/gen.Pt()),weight)
						
				for itrk, trk in enumerate(c.tracks):
					if not (abs(trk.Eta()) < 1.4442): continue#< 1.4442): continue
					if abs(trk.Eta()) < 1.566 and abs(trk.Eta()) > 1.4442: continue
					if not trk.Pt() > 15: continue
					if not isBaselineTrack(trk, itrk): continue
					if not isDisappearingTrack(trk, itrk): continue	  
					dr = gen.DeltaR(trk)
					if dr < drsmal:
						drsmal = dr
						idtrk  = itrk
						dtTlvsum = trk
				if drsmal < .01:
					fillth1(hEleGenPtDTeff, c.tracks[idtrk].Pt(), weight)
					fillth1(hEleGenEtaDTeff, abs(c.tracks[idtrk].Eta()), weight)
					fillth2(hGenPtvsResp, math.log10(c.tracks[idtrk].Pt()/gen.Pt()),gen.Pt(),weight)
					length = determineSML(dtTlvsum, idtrk)
					if (length == 1):
						fillth1(hEleGenPtSDTeff, c.tracks[idtrk].Pt(), weight)
						fillth1(hEleGenEtaSDTeff, abs(c.tracks[idtrk].Eta()), weight)
						fillth2(hGenPtvsRespS, gen.Pt(),math.log10(c.tracks[idtrk].Pt()/gen.Pt()),weight)
					if (length == 2):
						fillth1(hEleGenPtMDTeff, c.tracks[idtrk].Pt(), weight)
						fillth1(hEleGenEtaMDTeff, abs(c.tracks[idtrk].Eta()), weight)
						fillth2(hGenPtvsRespM, gen.Pt(),math.log10(c.tracks[idtrk].Pt()/gen.Pt()),weight)
					if (length == 3):
						fillth1(hEleGenPtLDTeff, c.tracks[idtrk].Pt(), weight)
						fillth1(hEleGenEtaLDTeff, abs(c.tracks[idtrk].Eta()), weight)
						fillth2(hGenPtvsRespL, gen.Pt(),math.log10(c.tracks[idtrk].Pt()/gen.Pt()),weight)
					
		theTag = TLorentzVector()
		theTag.SetPxPyPzE(0,0,0,0)						
		if len(tightElectrons)==1:
			C1 = tightElectrons[0][1]
			P1 = tightElectrons[0][0].Pt()#mu.Pt()
			Eta1 = tightElectrons[0][0].Eta()#abs(mu.Eta())
			Phi1 = tightElectrons[0][0].Phi()#mu.Phi()
			theTag = tightElectrons[0][0]
		elif len(tightElectrons)>1:
			try: r = int(1000*sf)%2+1
			except: 
				r = random.randint(1,2)
				#print 'you shouldnt see this more than once per job'
			#r = random.randint(1,2)
			if r==1:
				C1 = tightElectrons[0][1]
				P1 = tightElectrons[0][0].Pt()#mu.Pt()
				Eta1 = tightElectrons[0][0].Eta()#abs(mu.Eta())
				Phi1 = tightElectrons[0][0].Phi()#mu.Phi()
				theTag = tightElectrons[0][0]
			else:
				C1 = tightElectrons[1][1]
				P1 = tightElectrons[1][0].Pt()#mu.Pt()
				Eta1 = tightElectrons[1][0].Eta()#abs(mu.Eta())
				Phi1 = tightElectrons[1][0].Phi()#mu.Phi()
				theTag = tightElectrons[1][0]
					
					
		if not theTag.Pt()>1: continue	
		probeIsEl, probeIsDt = False, False
		dIMmax = 999
		for itrack, track in enumerate(c.tracks):
			if not (track.Pt() > 15): continue
			if not (abs(track.Eta()) < 1.4442): continue
			if abs(track.Eta()) < 1.566 and abs(track.Eta()) > 1.4442: continue
			if track.DeltaR(theTag)<0.01: continue		
			if not isBaselineTrack(track, itrack): continue				
			if not isDisappearingTrack(track, itrack): continue
			tagProbeTlvSum = theTag + track
			IMleplep = tagProbeTlvSum.M()
			if (IMleplep < 0): continue
			dIM = abs(IMleplep - 91)
			if(dIM < dIMmax):
					dIMmax = dIM
					IM     = IMleplep
					track_id  = itrack
					probeTlv =  track
					C2 = c.tracks_charge[itrack]
					probeIsDt = True
					probeIsEl = False
								
		for ireco, reco in enumerate(c.Electrons):
			if not (abs(reco.Eta()) < 1.4442): continue#< 1.4442)): continue
			if abs(reco.Eta()) < 1.566 and abs(reco.Eta()) > 1.4442: continue
			if reco.DeltaR(theTag)<0.01: continue
			if not (reco.Pt() > 10 and bool(c.Electrons_tightID[ireco]) ==1): continue
			drBig4Trk = 9999
			for trk in basicTracks:
				drTrk = trk.DeltaR(reco)
				if drTrk<drBig4Trk:
					drBig4Trk = drTrk
					if drBig4Trk<0.01: break
			if not drBig4Trk<0.01: continue		

			if (C1 + c.Electrons_charge[ireco] ==0):
					tagProbeTlvSum = theTag + reco
					fillth1(hIMmuZ, tagProbeTlvSum.M(), weight)
			sf = 1 #0**(sfHist.GetRandom())
			#sf = getSF(abs(c.Electrons[ireco].Eta()), min(c.Electrons[ireco].Pt(),309.999))
			smearedEleProbe.SetPtEtaPhiE(sf*c.Electrons[ireco].Pt(),c.Electrons[ireco].Eta(),c.Electrons[ireco].Phi(),sf*c.Electrons[ireco].E())
			if not smearedEleProbe.Pt()>15: continue
			tagProbeTlvSum = theTag + smearedEleProbe
			IMleplep = tagProbeTlvSum.M()
			if (C1 + c.Electrons_charge[ireco] ==0):
					fillth1(hIMmuZsmear, tagProbeTlvSum.M(), weight)
			if (IMleplep < 0): continue
			dIM = abs(IMleplep - 91)
			if(dIM < dIMmax):
				dIMmax = dIM
				IM     = IMleplep
				track_id  = ireco
				probeTlv =  reco
				C2 = c.Electrons_charge[ireco]
				probeIsEl = True
				probeIsDt = False						


		if (IM > 60 and IM < 120 and (C1+C2 )==0):
			#print ientry, '', dIMmax, 'inv mass', IM, 'track_id', track_id, 'probeIsDt', probeIsDt, 'probeIsEl', probeIsEl												
			if probeIsDt:
				P2 = probeTlv.Pt()
				Eta2 = abs(probeTlv.Eta())
				fillth1(hEleTagPt, P1, weight)
				fillth1(hEleProbePt, P2, weight)
				fillth1(hEleTagEta, Eta1, weight)
				fillth1(hEleProbeEta, Eta2, weight)
				print ientry, 'inside disappearing track', IM		
				fillth1(hIMZ, IM, weight)
				fillth1(hIMZDTmeff, IM, weight)
				fillth1(hEleProbePtDTmeff, P2, weight)
				fillth1(hEleProbeEtaDTmeff, Eta2, weight)
#				gm  = genMatch(probeTlv)

				fillth1(hIMZDTeff, IM, weight)
				fillth1(hEleProbePtDTeff, P2, weight)
				fillth1(hEleProbeEtaDTeff, Eta2, weight)
				fillth2(hRelErrPtvsptTrk, P2,c.tracks_ptError[track_id]/(P2*P2),weight)
				length = determineSML(probeTlv, track_id)
				if (length == 1):
						fillth1(hEleProbePtSDTeff, P2, weight)
						fillth1(hEleProbeEtaSDTeff, Eta2, weight)
				if (length == 2):
						fillth1(hEleProbePtMDTeff, P2, weight)
						fillth1(hEleProbeEtaMDTeff, Eta2, weight)
				if (length == 3):
						fillth1(hEleProbePtLDTeff, P2, weight)
						fillth1(hEleProbeEtaLDTeff, Eta2, weight)
			if probeIsEl:
				fillth1(hIMZ, IM, weight)##try to use this to get counts
				P2   = probeTlv.Pt()
				Eta2 = abs(probeTlv.Eta())
			
				fillth1(hEleTagPt, P1, weight)
				fillth1(hEleProbePt, P2, weight)
				fillth1(hEleTagEta, Eta1, weight)
				fillth1(hEleProbeEta, Eta2, weight)
				fillth1(hIMZRECOeff, IM, weight)
				fillth1(hEleProbePtRECOeff, P2, weight)
				fillth1(hEleProbeEtaRECOeff, Eta2, weight)
				recof = 1				

	print "RECOing probe", f , "DTing probes", n

	fnew = TFile('TagnProbeEleHists_'+identifier+'.root','recreate')
        print 'making', 'TagnProbeEleHists_'+identifier+'.root'
        fnew.cd()

	hIMcheck.Write()
	hHTnum.Write()

	hEleGenPt.Write()
	hEleGenEta.Write()

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
	hEleTagPt.Write()
	hEleTagEta.Write()

	hEleProbePt.Write()
	hEleProbeEta.Write()
	hIMZ.Write()
	hIMmuZsmear.Write()
	hIMmuZ.Write()
	hprobe.Write()

	hIMZRECOeff.Write()
	hEleProbePtRECOeff.Write()
	hEleProbeEtaRECOeff.Write()
	hIMZDTeff.Write()
	hEleProbePtDTeff.Write()
	hEleProbeEtaDTeff.Write()
	hEleProbePtSDTeff.Write()
	hEleProbeEtaSDTeff.Write()
	hEleProbePtMDTeff.Write()
	hEleProbeEtaMDTeff.Write()
	hEleProbePtLDTeff.Write()
	hEleProbeEtaLDTeff.Write()

	#response
	hmuonresp.Write()
	hmuonresptest.Write()
	hRelErrPtvsptTrk.Write()

	hGenPtvsResp.Write()
	hGenPtvsRespS.Write()
	hGenPtvsRespM.Write()
	hGenPtvsRespL.Write()
	hne.Write()
	print "just created file:", fnew.GetName()
	fnew.Close()


def genMatch(lep):
	for igenm, genm in enumerate(c.GenParticles):
		if not (abs(c.GenParticles_PdgId[igenm]) == 11 and c.GenParticles_Status[igenm] == 1):continue
		drm = genm.DeltaR(lep)
		if drm < .01:
			return 1
	return 0
def determineSML(sp_track, sp_track_id):
	S = 0
	M = 0
	L = 0
	if c.tracks_pixelLayersWithMeasurement[sp_track_id] == c.tracks_trackerLayersWithMeasurement[sp_track_id]: S = 1
	if c.tracks_trackerLayersWithMeasurement[sp_track_id] < 7 and c.tracks_pixelLayersWithMeasurement[sp_track_id] < c.tracks_trackerLayersWithMeasurement[sp_track_id]: M = 2
	if c.tracks_trackerLayersWithMeasurement[sp_track_id] > 6 and c.tracks_pixelLayersWithMeasurement[sp_track_id] < c.tracks_trackerLayersWithMeasurement[sp_track_id]: L = 3
	return S+M+L
		
def isBaselineTrack(track, track_id):
	flag = 1
	if not (track.Pt()>10 and abs(track.Eta())<1.4442): return 0
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

def nJets_adj(muon):

	j = c.NJets
	for ijet, jet in enumerate(c.Jets):
		if (c.NJets == ijet): break
		print "Jet number ", ijet+1, " Pt: ", jet.Pt()
		dr = muon.DeltaR(jet)
		if (dr < 0.5): j = j-1
	return j
		

def getSF(Eta, Pt):
	for histkey in  dResponseHist:
		if Eta > histkey[0][0] and Eta < histkey[0][1] and Pt > histkey[1][0] and Pt < histkey[1][1]:
			return 10**(dResponseHist[histkey].GetRandom())
	return 1


main()

