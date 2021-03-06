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

fname = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDII/CMSSW_8_0_20/src/TagProbeTrees/TemplateSplit.root'
f  = TFile(fname)
keys = f.GetListOfKeys()
sfHist   = f.Get('htrkresp')
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
hEleProbePtDTmeff      = TH1D("hEleProbePtDTmeff", "pt of the EleProbes", len(m)-1,np.asarray(m, 'd'))
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
#	print 'file number:', f, ':',inputFiles[f]
#	c.Add(inputFiles[f])

#c.Add(inputFiles[0])

nentries = c.GetEntries()
print "will process", nentries, "events"

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
        c.GetEntry(ientry)
        hHTnum.Fill(c.madHT)
	flag_probe = -1
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
	muTlvsum = TLorentzVector()
	muTlvsum.SetPxPyPzE(0, 0, 0, 0)
        trkTlvsum = TLorentzVector()
        trkTlvsum.SetPxPyPzE(0, 0, 0, 0)
	smearTlvsum = TLorentzVector()
        smearTlvsum.SetPtEtaPhiE(0, 0, 0, 0)
        smearTlv = TLorentzVector()
        smearTlv.SetPtEtaPhiE(0, 0, 0, 0)
        chiTlvsum = TLorentzVector()
        chiTlvsum.SetPxPyPzE(0, 0, 0, 0)
	dtTlvsum = TLorentzVector()
        dtTlvsum.SetPxPyPzE(0, 0, 0, 0)
        checkTlvsum = TLorentzVector()
        checkTlvsum.SetPxPyPzE(0, 0, 0, 0)
	ne = 0
	chargeCheck = 0
	for ie, e in enumerate(c.Electrons):
		if (e.Pt() < 30 or c.Electrons_tightID[ie] ==0): continue
		ne = ne + 1
		if ie > 1: continue
		chargeCheck =chargeCheck + c.Electrons_charge[ie]
		checkTlvsum = checkTlvsum + e
	hne.Fill(ne, (c.CrossSection*35.9)/(1*.001))
	if (chargeCheck == 0):
		hIMcheck.Fill(checkTlvsum.M(), (c.CrossSection*35.9)/(1*.001))
	if ne == 1 : e1 +=1
	if ne == 2 : e2 +=1
	if ne >  2 : e3 +=1
        for igen, gen in enumerate(c.GenParticles):
		if 1 < 2:
			drsmall = .2
			drsmal  = .2
			idtrk   = -1
			idlep   = -1
			if not (gen.Pt() > 10 and 2.4 > abs(gen.Eta()) > 1.566): continue
			if not (abs(c.GenParticles_PdgId[igen]) == 11 and c.GenParticles_Status[igen] == 1):continue
		
			hEleGenPt.Fill(gen.Pt(), (c.CrossSection*35.9)/(1*.001))
			hEleGenEta.Fill(abs(gen.Eta()), (c.CrossSection*35.9)/(1*.001))
			for im, m in enumerate(c.Electrons):
				if not (m.Pt() > 10 and 2.4 > abs(m.Eta()) and abs(m.Eta()) > 1.566 ): continue
				dr = gen.DeltaR(m)
				if dr < drsmall:
					drsmall = dr
					idlep   = im
			if drsmall < .01:
				sf = 10**(sfHist.GetRandom())
				smearTlvsum.SetPtEtaPhiE(sf*c.Electrons[idlep].Pt(),c.Electrons[idlep].Eta(),c.Electrons[idlep].Phi(),sf*c.Electrons[idlep].E())
				hEleGenPtRECOeff.Fill(smearTlvsum.Pt(), (c.CrossSection*35.9)/(1*.001))
				hEleGenEtaRECOeff.Fill(abs(c.Electrons[idlep].Eta()), (c.CrossSection*35.9)/(1*.001))
				hmuonresp.Fill(math.log10(c.Electrons[idlep].Pt()/gen.Pt()),(c.CrossSection*35.9)/(1*.001))
			#	sf = 10**(sfHist.GetRandom())
			#	smearTlvsum.SetPtEtaPhiE(sf*c.Electrons[idlep].Pt(),c.Electrons[idlep].Eta(),c.Electrons[idlep].Phi(),sf*c.Electrons[idlep].E())
				#print 10*'**','Pt',c.Electrons[idlep].Pt(),'smeared Pt',smearTlvsum.Pt()
				hmuonresptest.Fill(math.log10(smearTlvsum.Pt()/gen.Pt()),(c.CrossSection*35.9)/(1*.001))
			for itrk, trk in enumerate(c.tracks):
				if not (2.4 > abs(trk.Eta()) and abs(trk.Eta()) > 1.566): continue
				if trk.Pt() < 10: continue
				dr = gen.DeltaR(trk)
				if dr < drsmal:
					drsmal = dr
					idtrk  = itrk
					dtTlvsum = trk

#			print ientry, drsmal
#			pause()
			if drsmal < .01:
#				print ientry, drsmal
#				pause()
				flag_probe = probe(dtTlvsum, idtrk)
				if (flag_probe == 1):
					print ientry, drsmal
					pause()
					hEleGenPtDTeff.Fill(c.tracks[idtrk].Pt(), (c.CrossSection*35.9)/(1*.001))
					hEleGenEtaDTeff.Fill(abs(c.tracks[idtrk].Eta()), (c.CrossSection*35.9)/(1*.001))
					htrkresp.Fill(math.log10(c.tracks[idtrk].Pt()/gen.Pt()),(c.CrossSection*35.9)/(1*.001))
					hGenPtvsResp.Fill(math.log10(c.tracks[idtrk].Pt()/gen.Pt()),gen.Pt(),(c.CrossSection*35.9)/(1*.001))
					length = trackSplit(dtTlvsum, idtrk)
					if (length == 1):
						htrkrespS.Fill(math.log10(c.tracks[idtrk].Pt()/gen.Pt()),(c.CrossSection*35.9)/(1*.001))
						hEleGenPtSDTeff.Fill(c.tracks[idtrk].Pt(), (c.CrossSection*35.9)/(1*.001))
						hEleGenEtaSDTeff.Fill(abs(c.tracks[idtrk].Eta()), (c.CrossSection*35.9)/(1*.001))
						hGenPtvsRespS.Fill(gen.Pt(),math.log10(c.tracks[idtrk].Pt()/gen.Pt()),(c.CrossSection*35.9)/(1*.001))
					if (length == 2):
						htrkrespM.Fill(math.log10(c.tracks[idtrk].Pt()/gen.Pt()),(c.CrossSection*35.9)/(1*.001))
						hEleGenPtMDTeff.Fill(c.tracks[idtrk].Pt(), (c.CrossSection*35.9)/(1*.001))
                                                hEleGenEtaMDTeff.Fill(abs(c.tracks[idtrk].Eta()), (c.CrossSection*35.9)/(1*.001))
						hGenPtvsRespM.Fill(gen.Pt(),math.log10(c.tracks[idtrk].Pt()/gen.Pt()),(c.CrossSection*35.9)/(1*.001))
					if (length == 3):
						htrkrespL.Fill(math.log10(c.tracks[idtrk].Pt()/gen.Pt()),(c.CrossSection*35.9)/(1*.001))
						hEleGenPtLDTeff.Fill(c.tracks[idtrk].Pt(), (c.CrossSection*35.9)/(1*.001))
                                                hEleGenEtaLDTeff.Fill(abs(c.tracks[idtrk].Eta()), (c.CrossSection*35.9)/(1*.001))
						hGenPtvsRespL.Fill(gen.Pt(),math.log10(c.tracks[idtrk].Pt()/gen.Pt()),(c.CrossSection*35.9)/(1*.001))
        for imu, mu in enumerate(c.Electrons):
		r = random.randint(1,2)
		if (mu.Pt() < 30 or c.Electrons_tightID[imu] ==0): continue
		if (imu == 0 and ne == 1 ):
			C1 = c.Electrons_charge[imu]
			P1 = mu.Pt()
			Eta1 = abs(mu.Eta())
			Phi1 = mu.Phi()
			nmu = imu
			muTlvsum = dumTlvsum +  mu
		if (imu == 1 and ne > 1 and r == 1):
			C1 = c.Electrons_charge[imu]
                        P1 = mu.Pt()
                        Eta1 = abs(mu.Eta())
                        Phi1 = mu.Phi()
                        nmu = imu
                        muTlvsum = dumTlvsum +  mu
			rand +=1
		if (imu == 0 and ne > 1 and r == 2):
			C1 = c.Electrons_charge[imu]
                        P1 = mu.Pt()
                        Eta1 = abs(mu.Eta())
                        Phi1 = mu.Phi()
                        nmu = imu
                        muTlvsum =  dumTlvsum + mu
			rand +=1
#		print 'P1', mu.Pt()
#		print ne, 'number of electrons'
#		print "Event number :", ientry,":", muTlvsum.M()
	if (0 ==0):
	#	nJet = nJets_adj(muTlvsum)
	#	pfMET = math.sqrt(c.MET*c.MET + P1*P1 + c.MET*P2*math.cos(c.METPhi-Phi1))

		for ireco, reco in enumerate(c.Electrons):
			if not (abs(reco.Eta() > 1.566)): continue
			if ireco == nmu: continue
			if (reco.Pt() < 10 or c.Electrons_tightID[ireco] ==0): continue
#			if (ireco == nmu): continue
#			print 'charge:', c.Electrons_charge[ireco]
#			print 'test P1', P1
#			print 'test P2', reco.Pt()
#			print 'test IM e', reco.M()
			if (C1 + c.Electrons_charge[ireco] ==0):
				trkTlvsum = muTlvsum + reco
				hIMmuZ.Fill(trkTlvsum.M(), (c.CrossSection*35.9)/(1*.001))
			sf = 10**(sfHist.GetRandom())
			smearTlv.SetPtEtaPhiE(sf*c.Electrons[ireco].Pt(),c.Electrons[ireco].Eta(),c.Electrons[ireco].Phi(),sf*c.Electrons[ireco].E())
			trkTlvsum = muTlvsum + smearTlv
			IMmumu = trkTlvsum.M()
			if (C1 + c.Electrons_charge[ireco] ==0):
				hIMmuZsmear.Fill(trkTlvsum.M(), (c.CrossSection*35.9)/(1*.001))
#			#print 'IM test', IMmumu
			if (IMmumu < 0): continue
			dIM = abs(IMmumu - 91)
			if(dIM < dIMmax):
				dIMmax = dIM
				IM     = IMmumu
				track_id  = ireco
				chiTlvsum =  reco
				C2 = c.Electrons_charge[ireco]
#		#print IM
#		#print 10*'*'
		if (IM > 60 and IM < 120  and (C1+C2 )==0):
			hIMZ.Fill(IM, (c.CrossSection*35.9)/(1*.001))
			P2   = chiTlvsum.Pt()
			Eta2 = abs(chiTlvsum.Eta())
			
			hEleTagPt.Fill(P1, (c.CrossSection*35.9)/(1*.001))
			hEleProbePt.Fill(P2, (c.CrossSection*35.9)/(1*.001))
			hEleTagEta.Fill(Eta1, (c.CrossSection*35.9)/(1*.001))
			hEleProbeEta.Fill(Eta2, (c.CrossSection*35.9)/(1*.001))
			hIMZRECOeff.Fill(IM, (c.CrossSection*35.9)/(1*.001))
			hEleProbePtRECOeff.Fill(P2, (c.CrossSection*35.9)/(1*.001))
			hEleProbeEtaRECOeff.Fill(Eta2, (c.CrossSection*35.9)/(1*.001))
			recof = 1
			continue
		dIMax = 9999
		for ichi, chi in enumerate(c.tracks):
			if not (abs(chi.Eta() > 1.566)): continue
#			#print 'trk charge:', c.tracks_charge[ichi]
			trkTlvsum = muTlvsum + chi
			IMmumu = trkTlvsum.M()
			if (IMmumu < 0): continue
			dIM = abs(IMmumu - 91)
			if(dIM < dIMmax):
				dIMmax = dIM
				IM     = IMmumu
				track_id  = ichi
				chiTlvsum =  chi
				C2 = c.tracks_charge[ichi]
#		#print "Chi candidate number", ichi , "in event", ientry , "mu mu invariant mass =", IM
		#print 'tracks', IM
                #print 10*'*'
		if (IM > 60 and IM < 120 and (C1+C2 )==0):
			P2 = chiTlvsum.Pt()
			Eta2 = abs(chiTlvsum.Eta())
			hEleTagPt.Fill(P1, (c.CrossSection*35.9)/(1*.001))
			hEleProbePt.Fill(P2, (c.CrossSection*35.9)/(1*.001))
                        hEleTagEta.Fill(Eta1, (c.CrossSection*35.9)/(1*.001))
                        hEleProbeEta.Fill(Eta2, (c.CrossSection*35.9)/(1*.001))
			flag_probe = probe(chiTlvsum, track_id)
			if (flag_probe == 1):
				hIMZ.Fill(IM, (c.CrossSection*35.9)/(1*.001))
				hIMZDTmeff.Fill(IM, (c.CrossSection*35.9)/(1*.001))
				hEleProbePtDTmeff.Fill(P2, (c.CrossSection*35.9)/(1*.001))
				hEleProbeEtaDTmeff.Fill(Eta2, (c.CrossSection*35.9)/(1*.001))
				gm  = genMatch(chiTlvsum)
				if gm == 1:
					hIMZDTeff.Fill(IM, (c.CrossSection*35.9)/(1*.001))
					hEleProbePtDTeff.Fill(P2, (c.CrossSection*35.9)/(1*.001))
					hEleProbeEtaDTeff.Fill(Eta2, (c.CrossSection*35.9)/(1*.001))
					hRelErrPtvsptTrk.Fill(P2,c.tracks_ptError[track_id]/(P2*P2),(c.CrossSection*35.9)/(1*.001))
					length = trackSplit(chiTlvsum, track_id)
					if (length == 1):
						hEleProbePtSDTeff.Fill(P2, (c.CrossSection*35.9)/(1*.001))
						hEleProbeEtaSDTeff.Fill(Eta2, (c.CrossSection*35.9)/(1*.001))
                                        if (length == 2):
						hEleProbePtMDTeff.Fill(P2, (c.CrossSection*35.9)/(1*.001))
						hEleProbeEtaMDTeff.Fill(Eta2, (c.CrossSection*35.9)/(1*.001))
                                        if (length == 3):
						hEleProbePtLDTeff.Fill(P2, (c.CrossSection*35.9)/(1*.001))
						hEleProbeEtaLDTeff.Fill(Eta2, (c.CrossSection*35.9)/(1*.001))
			t.GetEntry(jentry)
			XsecLumi[0]       = (c.CrossSection)/(1*0.001)
			tagPt[0]          = P1
			probePt[0]        = P2
			tagEta[0]         = Eta1
			probeEta[0]       = Eta2
			IMz[0]            = IM
			if (flag_probe == 0):
				IMzDT[0]              = IM
				probePtDT[0]          = P2
				probeEtaDT[0]         = Eta2
				probePtRECO[0]        = -1
				probeEtaRECO[0]       = -1
				IMzRECO[0]            = -1
			if (flag_probe == 1):
				IMzRECO[0]            = IM
				probePtRECO[0]        = P2
				probeEtaRECO[0]       = Eta2
				probePtDT[0]          = -1
                                probeEtaDT[0]         = -1
				IMzDT[0]              = -1
			DTprobe[0]        = flag_probe
			jentry += 1
			t.Fill()
    #print 'Event with 1 e:', e1 ,'Event with 2 e:', e2,'Event with 3 e:', e3
#    ftp  = TFile('TagnProbeEleTree_'+identifier+'.root','recreate')
    t.Write()
    ftp.Close()
    print "file:", ftp , "created."
    print "RECOing probe", f , "DTing probes", n
    fnew = TFile('TagnProbeEleHists_'+identifier+'.root','recreate')
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
    htrkresp.Write()
    hmuonresp.Write()
    hmuonresptest.Write()
    hRelErrPtvsptTrk.Write()

    hGenPtvsResp.Write()
    hGenPtvsRespS.Write()
    hGenPtvsRespM.Write()
    hGenPtvsRespL.Write()
    hne.Write()
    fnew.Close()
    print "file:", fnew, "created."


    ftem = TFile('Template_Hists'+identifier+'.root','recreate')
    ftem.cd()
    htrkresp.Write()
    htrkrespS.Write()
    htrkrespM.Write()
    htrkrespL.Write()
    hmuonresp.Write()
    ftem.Close()
    print "file:", ftem, "created."
    

def genMatch(lep):
	for igenm, genm in enumerate(c.GenParticles):
		if not (abs(c.GenParticles_PdgId[igenm]) == 11 and c.GenParticles_Status[igenm] == 1):continue
		drm = genm.DeltaR(lep)
		if drm < .01:
			return 1
	return 0
def trackSplit(sp_chi, sp_chi_id):
        S = 0
        M = 0
        L = 0
	if c.tracks_pixelLayersWithMeasurement[sp_chi_id] == c.tracks_trackerLayersWithMeasurement[sp_chi_id]: S = 1
        if c.tracks_trackerLayersWithMeasurement[sp_chi_id] < 7 and c.tracks_pixelLayersWithMeasurement[sp_chi_id] < c.tracks_trackerLayersWithMeasurement[sp_chi_id]: M = 2
        if c.tracks_trackerLayersWithMeasurement[sp_chi_id] > 6 and c.tracks_pixelLayersWithMeasurement[sp_chi_id] < c.tracks_trackerLayersWithMeasurement[sp_chi_id]: L = 3
	return S+M+L
def probe(track, track_id):
	S = 0
	M = 0
	L = 0
	flag = 1
	if not (track.Pt() > 15): flag = 0
	if c.tracks_pixelLayersWithMeasurement[track_id] == c.tracks_trackerLayersWithMeasurement[track_id]: S = 1
	if c.tracks_trackerLayersWithMeasurement[track_id] < 7 and c.tracks_pixelLayersWithMeasurement[track_id] < c.tracks_trackerLayersWithMeasurement[track_id] : M = 2
	if c.tracks_trackerLayersWithMeasurement[track_id] > 6 and c.tracks_pixelLayersWithMeasurement[track_id] < c.tracks_trackerLayersWithMeasurement[track_id]: L = 3
	if track.Pt() < 15 or abs(track.Eta()) > 1.4442 : flag = 0
	if c.tracks_dxyVtx[track_id] > 0.02 and S == 1: flag = 0
	if c.tracks_dxyVtx[track_id] > 0.01 and S == 0: flag = 0
	if c.tracks_dzVtx[track_id]  > 0.05 : flag = 0
	if c.tracks_neutralPtSum[track_id] > 10 or ((c.tracks_neutralPtSum[track_id]/track.Pt()) > 0.1): flag = 0
	if c.tracks_chargedPtSum[track_id] > 10 or ((c.tracks_chargedPtSum[track_id]/track.Pt()) > 0.1): flag = 0
	if not c.tracks_passPFCandVeto[track_id]:flag = 0
	if not (c.tracks_trkRelIso[track_id] < 0.2): flag = 0
	if not (c.tracks_trkRelIso[track_id]*track.Pt() < 10) : flag = 0
	if c.tracks_trackerLayersWithMeasurement[track_id] < 2 or c.tracks_nValidTrackerHits[track_id] < 2 : flag = 0
	if c.tracks_nMissingInnerHits[track_id] > 0: flag = 0
	if c.tracks_nMissingOuterHits[track_id] < 2 and S == 0: flag = 0
	if c.tracks_ptError[track_id]/(track.Pt()*track.Pt()) > 0.2 and S == 1: flag = 0
	if c.tracks_ptError[track_id]/(track.Pt()*track.Pt()) > 0.05 and M == 2: flag = 0
	if c.tracks_ptError[track_id]/(track.Pt()*track.Pt()) > 0.005 and L == 3: flag = 0
	if not c.tracks_trackQualityHighPurity[track_id] : flag = 0
	
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

