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
import random



gROOT.SetBatch()
gROOT.SetStyle('Plain')

fname = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDII/CMSSW_8_0_20/src/TagProbeTrees/BarrelTemplates.root'
f  = TFile(fname)
keys = f.GetListOfKeys()
sfHist   = f.Get('htrkresp')#htrkrespL
#Histograms
m = [15, 30, 50, 70, 90, 120, 200, 300, 310]
eta = [0,1.4442,1.566,2.4]
hEleGenPt             = TH1D("hEleGenPt", ";m [GeV] ;pt of the gen Ele;;", len(m)-1,np.asarray(m, 'd'))
histoStyler(hEleGenPt,1)
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
hEleProbePt           = TH1D("hEleProbePt", "pt of the EleProbes", len(m)-1,np.asarray(m, 'd'))
hEleProbePtDTeff      = TH1D("hEleProbePtDTeff", "pt of the EleProbes", len(m)-1,np.asarray(m, 'd'))
hEleProbePtSDTeff      = TH1D("hEleProbePtSDTeff", "pt of the EleProbes", len(m)-1,np.asarray(m, 'd'))
hEleProbePtMDTeff      = TH1D("hEleProbePtMDTeff", "pt of the EleProbes", len(m)-1,np.asarray(m, 'd'))
hEleProbePtLDTeff      = TH1D("hEleProbePtLDTeff", "pt of the EleProbes", len(m)-1,np.asarray(m, 'd'))
hEleProbePtRECOeff    = TH1D("hEleProbePtRECOeff", "pt of the EleProbes", len(m)-1,np.asarray(m, 'd'))
#hEleProbePtDTmeff      = TH1D("hEleProbePtDTmeff", "pt of the EleProbes", len(m)-1,np.asarray(m, 'd'))
histoStyler(hEleProbePt,1)
histoStyler(hEleProbePtDTeff,1)
histoStyler(hEleProbePtSDTeff,1)
histoStyler(hEleProbePtMDTeff,1)
histoStyler(hEleProbePtLDTeff,1)
histoStyler(hEleProbePtRECOeff,1)
hEleProbeEta          = TH1D("hEleProbeEta", "Eta of the EleProbes", len(eta)-1,np.asarray(eta, 'd'))
hEleProbeEtaDTeff     = TH1D("hEleProbeEtaDTeff", "Eta of the EleProbes", len(eta)-1,np.asarray(eta, 'd'))
hEleProbeEtaSDTeff     = TH1D("hEleProbeEtaSDTeff", "Eta of the EleProbes", len(eta)-1,np.asarray(eta, 'd'))
hEleProbeEtaMDTeff     = TH1D("hEleProbeEtaMDTeff", "Eta of the EleProbes", len(eta)-1,np.asarray(eta, 'd'))
hEleProbeEtaLDTeff     = TH1D("hEleProbeEtaLDTeff", "Eta of the EleProbes", len(eta)-1,np.asarray(eta, 'd'))
hEleProbeEtaDTmeff     = TH1D("hEleProbeEtaDTmeff", "Eta of the EleProbes", len(eta)-1,np.asarray(eta, 'd'))
hEleProbeEtaRECOeff   = TH1D("hEleProbeEtaRECOeff", "Eta of the EleProbes", len(eta)-1,np.asarray(eta, 'd'))
histoStyler(hEleProbeEta,1)
histoStyler(hEleProbeEtaDTeff,1)
histoStyler(hEleProbeEtaSDTeff,1)
histoStyler(hEleProbeEtaMDTeff,1)
histoStyler(hEleProbeEtaLDTeff,1)
histoStyler(hEleProbeEtaDTmeff,1)
histoStyler(hEleProbeEtaRECOeff,1)
hEleTagPt             = TH1D("hEleTagPt"  , "pt of the EleTags", len(m)-1,np.asarray(m, 'd'))
hEleTagEta            = TH1D("hEleTagEta"  , "Eta of the EleTags", len(eta)-1,np.asarray(eta, 'd'))
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
hIMcheck                  = TH1D("hIMcheck"  , "IM  ", 60, 20, 180)
histoStyler(hIMcheck,1)

hIMZRECOeff           = TH1D("hIMZRECOeff"  , "IM tag + RECOing probe ", 40, 60, 120)
histoStyler(hIMZRECOeff,1)
hIMZDTeff             = TH1D("hIMZDTeff"  , "IM tag + DTing probe ", 40, 60, 120)
histoStyler(hIMZDTeff,1)

hIMZDTmeff            = TH1D("hIMZDTmeff"  , "IM tag + DTing probe ", 40, 60, 120)

histoStyler(hIMZDTmeff,1)

hHTnum                = TH1D("hHTnum","HT for number of events", 150,40,2500)

histoStyler(hHTnum,1)


hmuonresp             =TH1D("hmuonresp","muon response", 50,-3,3.2)
histoStyler(hmuonresp,1)
hmuonresptest         =TH1D("hmuonresptest","muon response test", 50,-3,3.2)
histoStyler(hmuonresptest,1)

hne                  = TH1F("hne", "number of electrons", 4, 0, 4)
histoStyler(hne,1)
#####
hRelErrPtvsptMu        = TH2D("hRelErrPtvsptMu","hRelErrPtvsptMu",50, 10, 400, 20, 0 ,2)
hRelErrPtvsptTrk       = TH2D("hRelErrPtvsptTrk","hRelErrPtvsptTrk",50, 10, 400, 20, 0 ,2)


hEleGenEtaSDTeff       = TH1D("hEleGenEtaSDTeff", "Eta of the SDT", len(eta)-1,np.asarray(eta, 'd'))
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

hEleProbePtDTmeff      = TH1D("hEleProbePtDTmeff", "pt of the EleProbes", len(m)-1,np.asarray(m, 'd'))
histoStyler(hEleProbePtDTmeff,1)

options = VarParsing ('python')
options.parseArguments()

#Input File 
inputFiles = options.inputFiles
if inputFiles ==  []:
		print 'running on small default DYtoLL sample'
		inputFiles = ["/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1_391_RA2AnalysisTree.root"]
c=TChain("TreeMaker2/PreSelection")
x = len(inputFiles)
#for f in range(0,x):
#        print 'file number:', f, ':',inputFiles[f]
#        c.Add(inputFiles[f])

#c.Add(inputFiles[0])

nentries = c.GetEntries()
verbosity = 1000

identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('Summer16.','').replace('RA2AnalysisTree','')
identifier+='nFiles'+str(len(inputFiles))

def main():

	for f in range(0,x):
			print 'file number:', f, ':',inputFiles[f]
			c.Add(inputFiles[f])

	nentries = c.GetEntries()
	print "will process", nentries, "events"
	ftp  = TFile('TagnProbeEleTree_'+identifier+'.root','recreate')
	t           = TTree('TagProbe','TagProbe')          #tree for tracks level optimization  
	XsecLumi      = np.zeros(1, dtype = float)
	b_XsecLumi    = t.Branch('XsecLumi', XsecLumi, 'XsecLumi/D')
	tagPt       = np.zeros(1, dtype = float)
	b_tagPt     = t.Branch('tagPt', tagPt, 'tagPt/D')
	probePt     = np.zeros(1, dtype = float)
	b_probePt   = t.Branch('probePt', probePt, 'probePt/D')
	probePtRECO     = np.zeros(1, dtype = float)
	b_probePtRECO   = t.Branch('probePtRECO', probePtRECO, 'probePtRECO/D')
	probePtDT     = np.zeros(1, dtype = float)
	b_probePtDT   = t.Branch('probePtDT', probePtDT, 'probePtDT/D')
	tagEta      = np.zeros(1, dtype = float)
	b_tagEta    = t.Branch('tagEta', tagEta, 'tagEta/D')
	probeEta    = np.zeros(1, dtype = float)
	b_probeEta  = t.Branch('probeEta', probeEta, 'probeEta/D')
	probeEtaRECO    = np.zeros(1, dtype = float)
	b_probeEtaRECO  = t.Branch('probeEtaRECO', probeEtaRECO, 'probeEtaRECO/D')
	probeEtaDT    = np.zeros(1, dtype = float)
	b_probeEtaDT  = t.Branch('probeEtaDT', probeEtaDT, 'probeEtaDT/D')
	IMzDT         = np.zeros(1, dtype = float)
	b_IMzDT       = t.Branch('IMzDT', IMzDT, 'IMzDT/D')
	IMzRECO         = np.zeros(1, dtype = float)
	b_IMzRECO       = t.Branch('IMzRECO', IMzRECO, 'IMzRECO/D')
	IMz         = np.zeros(1, dtype = float)
	b_IMz       = t.Branch('IMz', IMz, 'IMz/D')

	DTprobe     = np.zeros(1, dtype = bool)
	b_DTprobe   = t.Branch('DTprobe', DTprobe, 'DTprobe/O')
	jentry=0
	n = 0
	f = 0
	rand = 1
	e1 = 0
	e2 = 0
	e3 = 0
	for ientry in range(nentries):
	
	
		if ientry%verbosity==0:
			print 'now processing event number', ientry
		c.GetEntry(ientry)
#		weight = (c.CrossSection*35.9)/(1*.001)
		weight = 1
		hHTnum.Fill(c.madHT)
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
		C2reco = 0
		IM  =  0
		IMreco = 0
		dIM =  0
		dIMmax = 999
		track_id = -1
		
		dumTlvsum = TLorentzVector()
		dumTlvsum.SetPxPyPzE(0, 0, 0, 0)
		theTag = TLorentzVector()
		theTag.SetPxPyPzE(0, 0, 0, 0)
		tagProbeTlvSum = TLorentzVector()
		tagProbeTlvSum.SetPxPyPzE(0, 0, 0, 0)
		smearedEleProbesum = TLorentzVector()
		smearedEleProbesum.SetPtEtaPhiE(0, 0, 0, 0)
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
			if not muon.Pt()>15: continue
			if not abs(muon.Eta())<1.4442: continue
			muons.append(muon)
		if not len(muons)==0: continue
		tightElectrons = []
		for ie, e in enumerate(c.Electrons):
				if (e.Pt() < 30 or c.Electrons_tightID[ie] ==0 or abs(e.Eta()) > 2.4): continue
				tightElectrons.append([e,c.Electrons_charge[ie]])
				ne = ne + 1
				if ie > 1: continue
				chargeCheck =chargeCheck + c.Electrons_charge[ie]
				checkTlvsum = checkTlvsum + e
		hne.Fill(ne, weight)
		if (chargeCheck == 0):
				hIMcheck.Fill(checkTlvsum.M(), weight)
		if ne == 1 : e1 +=1
		if ne == 2 : e2 +=1
		if ne >  2 : e3 +=1

                basicTracks = []
                for itrack, track in enumerate(c.tracks):
                        if not isBaselineTrack(track, itrack): continue
                        basicTracks.append(track)


		for igen, gen in enumerate(c.GenParticles):
				if 1 < 2:
						drsmall = .2
						drsmal  = .2
						idtrk   = -1
						idlep   = -1
						if not (gen.Pt() > 10 and abs(gen.Eta()) < 1.4442): continue
						if not (abs(c.GenParticles_PdgId[igen]) == 11 and c.GenParticles_Status[igen] == 1):continue
			
						hEleGenPt.Fill(gen.Pt(), weight)
						hEleGenEta.Fill(abs(gen.Eta()), weight)
						for im, m in enumerate(c.Electrons):
								if not (m.Pt() > 10 and abs(m.Eta()) < 1.4442 ): continue

                                                                drBig4Trk = 9999
                                                                for trk in basicTracks:
                                                                        drTrk = trk.DeltaR(c.Electrons[im])
                                                                        if drTrk < drBig4Trk:
                                                                                drBig4Trk = drTrk
                                                                                if drTrk<0.01: break
                                                                if not drBig4Trk<0.01: continue

								dr = gen.DeltaR(m)
								if dr < drsmall:
									drsmall = dr
									idlep   = im
						if drsmall < .01:
								sf = 10**(sfHist.GetRandom())
								smearedEleProbesum.SetPtEtaPhiE(sf*c.Electrons[idlep].Pt(),c.Electrons[idlep].Eta(),c.Electrons[idlep].Phi(),sf*c.Electrons[idlep].E())
								if not smearedEleProbesum.Pt() > 15: continue
								hEleGenPtRECOeff.Fill(smearedEleProbesum.Pt(), weight)
								hEleGenEtaRECOeff.Fill(abs(c.Electrons[idlep].Eta()), weight)
								hmuonresp.Fill(math.log10(c.Electrons[idlep].Pt()/gen.Pt()),weight)
						#        sf = 10**(sfHist.GetRandom())
						#        smearedEleProbesum.SetPtEtaPhiE(sf*c.Electrons[idlep].Pt(),c.Electrons[idlep].Eta(),c.Electrons[idlep].Phi(),sf*c.Electrons[idlep].E())
								#print 10*'**','Pt',c.Electrons[idlep].Pt(),'smeared Pt',smearedEleProbesum.Pt()
								hmuonresptest.Fill(math.log10(smearedEleProbesum.Pt()/gen.Pt()),weight)
						for itrk, trk in enumerate(c.tracks):
								if not (abs(trk.Eta()) < 1.4442): continue
								if not (trk.Pt() > 15): continue
								if not isBaselineTrack(trk, itrk): continue
								dr = gen.DeltaR(trk)
								if dr < drsmal:
										drsmal = dr
										idtrk  = itrk
										dtTlvsum = trk
						if drsmal < .01:
								flag_DT = isDisappearingTrack(dtTlvsum, idtrk)
								if (flag_DT == 1):
										hEleGenPtDTeff.Fill(c.tracks[idtrk].Pt(), weight)
										hEleGenEtaDTeff.Fill(abs(c.tracks[idtrk].Eta()), weight)
										hGenPtvsResp.Fill(math.log10(c.tracks[idtrk].Pt()/gen.Pt()),gen.Pt(),weight)
										length = determineSML(dtTlvsum, idtrk)
										if (length == 1):
												hEleGenPtSDTeff.Fill(c.tracks[idtrk].Pt(), weight)
												hEleGenEtaSDTeff.Fill(abs(c.tracks[idtrk].Eta()), weight)
												hGenPtvsRespS.Fill(gen.Pt(),math.log10(c.tracks[idtrk].Pt()/gen.Pt()),weight)
										if (length == 2):
												hEleGenPtMDTeff.Fill(c.tracks[idtrk].Pt(), weight)
												hEleGenEtaMDTeff.Fill(abs(c.tracks[idtrk].Eta()), weight)
												hGenPtvsRespM.Fill(gen.Pt(),math.log10(c.tracks[idtrk].Pt()/gen.Pt()),weight)
										if (length == 3):
												hEleGenPtLDTeff.Fill(c.tracks[idtrk].Pt(), weight)
												hEleGenEtaLDTeff.Fill(abs(c.tracks[idtrk].Eta()), weight)
												hGenPtvsRespL.Fill(gen.Pt(),math.log10(c.tracks[idtrk].Pt()/gen.Pt()),weight)
#		if not ientry == 4207: continue			
		theTag = TLorentzVector()
		theTag.SetPxPyPzE(0,0,0,0)						
		if len(tightElectrons)==1:
						C1 = tightElectrons[0][1]
						P1 = tightElectrons[0][0].Pt()#mu.Pt()
						Eta1 = tightElectrons[0][0].Eta()#abs(mu.Eta())
						Phi1 = tightElectrons[0][0].Phi()#mu.Phi()
						theTag = tightElectrons[0][0]
		elif len(tightElectrons)>1:
			r = int(1000*sf)%2+1

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
		dIMmax = 9999
		for itrack, track in enumerate(c.tracks):
				if not (abs(track.Eta()) < 1.4442): continue
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
		dIMmaxreco = 9999
                for ireco, reco in enumerate(c.Electrons):
                                if not (abs(reco.Eta()) < 1.4442): continue
                                if reco.DeltaR(theTag)<0.001: continue
                                if not (reco.Pt() > 10 or c.Electrons_tightID[ireco] ==1): continue
                                drBig4Trk = 9999
                                for trk in basicTracks:
                                        drTrk = trk.DeltaR(reco)
                                        if drTrk<drBig4Trk:
                                                drBig4Trk = drTrk
                                                if drBig4Trk<0.01: break
                                if not drBig4Trk<0.01: continue 
                                if (C1 + c.Electrons_charge[ireco] ==0):
                                                tagProbeTlvSum = theTag + reco
                                                hIMmuZ.Fill(tagProbeTlvSum.M(), weight)
                                sf = 10**(sfHist.GetRandom())
                                smearedEleProbe.SetPtEtaPhiE(sf*c.Electrons[ireco].Pt(),c.Electrons[ireco].Eta(),c.Electrons[ireco].Phi(),sf*c.Electrons[ireco].E())
                                if not (smearedEleProbe.Pt() > 15) : continue
                                tagProbeTlvSum = theTag + smearedEleProbe
                                IMleplep = tagProbeTlvSum.M()
                                if (C1 + c.Electrons_charge[ireco] ==0):
                                                hIMmuZsmear.Fill(tagProbeTlvSum.M(), weight)
                                if (IMleplep < 0): continue
                                dIM = abs(IMleplep - 91)
                                if(dIM < dIMmaxreco):
                                                dIMmaxreco = dIM
                                                IMreco     = IMleplep
                                                track_idreco  = ireco
                                                probeTlvreco =  reco
                                                C2reco = c.Electrons_charge[ireco]
		print ientry, dIMmaxreco, dIMmax, 'IM trk', IM, 'IM reco', IMreco, C1+C2
		pause()
		
		if (dIMmax < dIMmaxreco and IM > 60 and IM < 120 and (C1+C2 )==0):
			        #print ientry, 'found DT', probeTlv.Pt()
				P2 = probeTlv.Pt()
				Eta2 = abs(probeTlv.Eta())
				hEleTagPt.Fill(P1, weight)
				hEleProbePt.Fill(P2, weight)
				hEleTagEta.Fill(Eta1, weight)
				hEleProbeEta.Fill(Eta2, weight)
				flag_DT = isDisappearingTrack(probeTlv, track_id)
				if (flag_DT == 1):
#					        #print ientry, 'found DT', probeTlv.Pt()
						hIMZ.Fill(IM, weight)
						hIMZDTmeff.Fill(IM, weight)
						hEleProbePtDTmeff.Fill(P2, weight)
						hEleProbeEtaDTmeff.Fill(Eta2, weight)
						gm  = genMatch(probeTlv)
						if gm == 1:
#							        #print ientry, 'found DT', probeTlv.Pt()
								hIMZDTeff.Fill(IM, weight)
								hEleProbePtDTeff.Fill(P2, weight)
								hEleProbeEtaDTeff.Fill(Eta2, weight)
								hRelErrPtvsptTrk.Fill(P2,c.tracks_ptError[track_id]/(P2*P2),weight)
								length = determineSML(probeTlv, track_id)
								if (length == 1):
										hEleProbePtSDTeff.Fill(P2, weight)
										hEleProbeEtaSDTeff.Fill(Eta2, weight)
								if (length == 2):
										hEleProbePtMDTeff.Fill(P2, weight)
										hEleProbeEtaMDTeff.Fill(Eta2, weight)
								if (length == 3):
										hEleProbePtLDTeff.Fill(P2, weight)
										hEleProbeEtaLDTeff.Fill(Eta2, weight)
				continue
                if (dIMmax > dIMmaxreco and IMreco > 60 and IMreco < 120  and (C1+C2reco )==0):
                                hIMZ.Fill(IMreco, weight)##try to use this to get counts                                                                                                                                  
                                P2   = probeTlv.Pt()
                                Eta2 = abs(probeTlv.Eta())

                                hEleTagPt.Fill(P1, weight)
                                hEleProbePt.Fill(P2, weight)
                                hEleTagEta.Fill(Eta1, weight)
                                hEleProbeEta.Fill(Eta2, weight)
                                hIMZRECOeff.Fill(IMreco, weight)
                                hEleProbePtRECOeff.Fill(P2, weight)
                                hEleProbeEtaRECOeff.Fill(Eta2, weight)
                                recof = 1
                                continue
				t.GetEntry(jentry)
				XsecLumi[0]       = (c.CrossSection)/(1*0.001)
				tagPt[0]          = P1
				probePt[0]        = P2
				tagEta[0]         = Eta1
				probeEta[0]       = Eta2
				IMz[0]            = IM
				if (flag_DT == 0):
						IMzDT[0]              = IM
						probePtDT[0]          = P2
						probeEtaDT[0]         = Eta2
						probePtRECO[0]        = -1
						probeEtaRECO[0]       = -1
						IMzRECO[0]            = -1
				if (flag_DT == 1):
						IMzRECO[0]            = IM
						probePtRECO[0]        = P2
						probeEtaRECO[0]       = Eta2
						probePtDT[0]          = -1
						probeEtaDT[0]         = -1
						IMzDT[0]              = -1
				DTprobe[0]        = flag_DT
				jentry += 1
				t.Fill()
	#print 'Event with 1 e:', e1 ,'Event with 2 e:', e2,'Event with 3 e:', e3
#    ftp  = TFile('TagnProbeEleTree_'+identifier+'.root','recreate')
	t.Write()
	ftp.Close()
	print "file:", ftp , "created."
	print "RECOing probe", f , "DTing probes", n
	fnew = TFile('TEST_TagnProbeEleHists_'+identifier+'.root','recreate')
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
			
main()

