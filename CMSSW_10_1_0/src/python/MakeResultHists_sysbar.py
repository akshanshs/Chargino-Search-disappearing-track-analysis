from ROOT import *
import os, sys
from glob import glob
import math
gStyle.SetOptStat(0)
#gROOT.SetBatch(1)
from time import sleep
#from utils import *
from utilitiesII_fabratio import *
lumi = 35900.0
istest = False

CombineLeptons_ = True
try: data_file = sys.argv[1]
except: data_file = 'Data_test2.root'
print data_file
Data = TFile(data_file)

try: prompt_file = sys.argv[2]          # same file for El and Mu
except: prompt_file = 'Prompt_test2.root' #'Prompt_promptv5aug.root' #'Prompt_test2.root'
print prompt_file
El = TFile(prompt_file)

#try: prompt_file = sys.argv[2]          # same file for El and Mu
#except: prompt_file = 'Prompt_test.root'
#print prompt_file
Mu = TFile(prompt_file)

try: fake_file = sys.argv[3]
except: fake_file = 'Fake_test2.root'
print fake_file
Fake = TFile(fake_file)

try: tau_file = sys.argv[4]
except: tau_file = 'Tau_test2.root'
print tau_file
Tau = TFile(tau_file)

try: fnameSig10 = sys.argv[5]
except: fnameSig10 = 'g1800_chi1400_27_200970_step4_10AODScaled13JuneNoSF.root'
sig10 = TFile(fnameSig10)

try: fnameSig30 = sys.argv[6]
except:fnameSig30 = 'g1800_chi1400_27_200970_step4_30AODScaled13JuneNoSF.root'
sig30 =TFile(fnameSig30)

try: fnameSig50 = sys.argv[7]
except:fnameSig50 = 'g1800_chi1400_27_200970_step4_50AODScaled13JuneNoSF.root'
sig50 =TFile(fnameSig50)

try: fnameSig100 = sys.argv[8]
except:fnameSig100 = 'g1800_chi1400_27_200970_step4_100AODScaled13JuneNoSF.root'
sig100 =TFile(fnameSig100)

try: fnameOut = sys.argv[9]
except: fnameOut = 'Result_hists.root'


Data.ls()     # base file to decide variables to be used

fnew2 = TFile(fnameOut,'recreate')

keys = Data.GetListOfKeys()

print 'len(keys)', len(keys)

print keys
pause()

SigFiles = [[sig10,'Signal','#chi^{#pm} c#tau=10 cm', 8,20],[sig30,'Signal','#chi^{#pm} c#tau=30 cm', 30,21],[sig50,'Signal','#chi^{#pm} c#tau=50 cm', 49,22],[sig100,'Signal','#chi^{#pm} c#tau=100 cm',43,34]]
BkgFiles = [[Tau,'Tau','prompt (#tau^{#pm})',6],[Fake,'Fake','non-prompt', 7],[Mu,'Mu','prompt (#mu^{#pm})',2],[El,'El','prompt (e^{#pm})',kBlue-6]]#,[Fake,'Fake','non-prompt', 7]]

#File name put in as list of list: [filename, histID, legname, color]

# Original script for closure edited as Method = stacked bkg hists, Control = Stacked Signals, Truth = Data

dBkgCompositionHist = {}
dSigCompositionHist = {}


for key in keys:#[:241]:
#	infile.cd()
	name = key.GetName()
	print name
	if not '_error' in name : continue
	basehistname = name.replace('_error','')
	print 'basehistname:',basehistname
	var = basehistname.split('Method')[0].split('_')[-1]
	print 'variable name = ', var
	hData = Data.Get(basehistname)    # play role like a truth hist
	hSum = hData.Clone('hSum')
	hSumStat = hData.Clone('hSumStat')
	hSum.Reset('')
	hSumStat.Reset('')
	hSum.Sumw2()
	hSumStat.Sumw2()
	stackhistsname = basehistname.replace('Data','').split('Method')[0]
	dBkgCompositionHist[stackhistsname] =  [THStack(stackhistsname,""), hSum, hSumStat]
	dSigCompositionHist[stackhistsname] =  THStack(stackhistsname,"")    # stackhists, add hist for ratio and error

	print 'stackhistsname: ',stackhistsname
	legbkg = mklegend(x1=.6, y1=.55, x2= 0.99, y2=.89, color=kWhite) #place to be adjusted later
	legsig = mklegend(x1=.15, y1=.6, x2= 0.62, y2=.89, color=kWhite) # place to be adjusted later

	bkgBinError2 = []   # contain array of err[i]^2 
	x_axis = hData.GetXaxis()
	for ibin in range(1,x_axis.GetNbins()+1): bkgBinError2.append(0)    # initialize the array to 0

	print 'Inition error square array: ', bkgBinError2
	for isig, sig in enumerate(SigFiles):   ####################################Stack Signal
		print 'Signal  file: ', sig
		histsig =  sig[0].Get(basehistname.replace('Data',sig[1]))
		print 'histobram: ', histsig
		histsig.Scale(.68)
		histsig.SetMarkerColor(sig[3])
		histsig.SetMarkerStyle(sig[4])
		histsig.SetMarkerSize(1.3)
		histsig.SetLineColorAlpha(sig[3],.5)
#		histsig.SetLineWidth(2)
#		histsig.SetFillStyle(4050)
#		histsig.line style marke style etc
		legsig.AddEntry(histsig,sig[2],'lep')
#		for ibin in range(1,x_axis.GetNbins()+1):
#			sigcontent = histsig.GetBinContent(ibin)
#			errorhist = sig[0].Get(basehistname.replace('Data',sig[1])+'_error')
#			errorhist.Scale(6.8)
#			syserror = errorhist.GetBinContent(ibin)
#			staterror = histsig.GetBinError(ibin)
#			binerror = math.sqrt((syserror*syserror) + (staterror*staterror))
#			histsig.SetBinError(ibin,binerror)
		dSigCompositionHist[stackhistsname].Add(histsig)

	#pause()
	for ibkg, bkg in enumerate(BkgFiles):     ####################################Stack and Add bkg
		print 'background file: ', bkg
		histbkg =  bkg[0].Get(basehistname.replace('Data',bkg[1]))
		dBkgCompositionHist[stackhistsname][1].Add(histbkg) # adding hists to get total hist with stat Sys is added later
		dBkgCompositionHist[stackhistsname][2].Add(histbkg) # adding hists to get total hist for ratio plot
		print 'histobram: ' , histbkg
		histbkg.SetFillColor(bkg[3])
		histbkg.SetLineWidth(1)
		histbkg.SetLineColor(1)
#		histbkg.Scale(1.0,'width')
		legbkg.AddEntry(histbkg,bkg[2],'f')
		dBkgCompositionHist[stackhistsname][0].Add(histbkg)    # stacking hists

		for ibin in range(1,x_axis.GetNbins()+1):
			errorhist = bkg[0].Get(basehistname.replace('Data',bkg[1])+'_error') # or use: error = bkg[0].Get(name.replace('Data',bkg[1]))
			error = errorhist.GetBinContent(ibin)
			bkgBinError2[ibin-1] = bkgBinError2[ibin-1] + (error*error)    # adding systematic error^2 for each bin # Sum(error^2 [ibin])

	print 'error array after bkg file loop', bkgBinError2
#	pause()

	dBkgCompositionHist[stackhistsname][1].SetLineColor(1)
	dBkgCompositionHist[stackhistsname][1].SetLineWidth(1)
	dBkgCompositionHist[stackhistsname][1].SetLineStyle(1)
	dBkgCompositionHist[stackhistsname][1].SetFillStyle(4050)
#	dBkgCompositionHist[stackhistsname][1].SetFillStyle(3008)
	for ibin in range(1,x_axis.GetNbins()+1):
		staterror = dBkgCompositionHist[stackhistsname][1].GetBinError(ibin) # statistical error on Added histogram
		binerror = math.sqrt((bkgBinError2[ibin-1]) + staterror*staterror) # sqrt(sys^2 + stat^2)

		dBkgCompositionHist[stackhistsname][1].SetBinError(ibin,binerror)

	
#	leg = mklegend(x1=.48, y1=.65, x2=.95, y2=.87, color=kWhite)   # just a pseudo legend ,  not using it
#	leg.SetTextSize(0.07)
#	legname = 'distrack'
	themax = 500*max([dSigCompositionHist[stackhistsname].GetMaximum(),dBkgCompositionHist[stackhistsname][1].GetMaximum(),hData.GetMaximum()])
	
	dBkgCompositionHist[stackhistsname][0].SetMinimum(0.1)
	dBkgCompositionHist[stackhistsname][0].SetMaximum(themax)
	dBkgCompositionHist[stackhistsname][1].GetYaxis().SetRangeUser(0.1,themax)
	hData.GetYaxis().SetRangeUser(0.1,themax)
	legbkg.AddEntry(hData,'Data','p')
	dSigCompositionHist[stackhistsname].SetMinimum(0.1)
	dSigCompositionHist[stackhistsname].SetMaximum(themax)
	c1 = mkcanvas('c_'+stackhistsname.replace('_',''))
	pause()
	hratio,hbkg,hsysUp,hsysDown = FabDrawPrediction(c1,legbkg, legsig,hData,dBkgCompositionHist[stackhistsname][0],dSigCompositionHist[stackhistsname],dBkgCompositionHist[stackhistsname][1],dBkgCompositionHist[stackhistsname][2],var,lumi=35.9,LinearScale=False, fraction = '#frac{data}{prediction}')
#	pause()
	hratio.GetYaxis().SetRangeUser(-0.005,2.6) #hmm
#	hratio.GetYaxis().SetRangeUser(0.09,99)
	hratio.SetLineColor(kBlack)
	hratio.SetMarkerColor(kBlack)
	c1.cd(2)
        c1.SetLogy()
        c1.Update()
	c1.Write()
#	pause()
	c1.Print('resulthists/'+stackhistsname.replace('_','')+'.png')
	c1.Delete()                                                                                                           
        hratio.Delete()
#	pause()
#	dBkgCompositionHist[stackhistsname][0].Draw("hist")
#	c1.Update()
	#pause()
#	dSigCompositionHist[stackhistsname].Draw("nostackhistsame")
#	c1.Update()
	#pause()
#	dBkgCompositionHist[stackhistsname][1].Draw("histsame e1")
#	c1.Update()
	#pause()
#	hData.Draw("same p")
#	pause()


print 'test a'


print 'test b'
print 'just created', os.getcwd()+'/'+fnew2.GetName()
fnew2.Close()
print 'test c'

'''

	hratio = FabDrawNew(c1,leg,hData,dBkgCompositionHist[stackhistsname][1],datamc='DATA',lumi=lumi, title = '', LinearScale=False, fractionthing='#frac{prediction}{data}') 
	#hratio.GetYaxis().SetRangeUser(0.0,2.5)
	hratio.GetYaxis().SetRangeUser(0.09,100)	
	hratio.SetLineColor(kBlack)
	hratio.SetMarkerColor(kBlack)
	c1.cd(2)
	c1.SetLogy()
	c1.Update()
	c1.cd(1)
	dBkgCompositionHist[stackhistsname][0].Draw("histsame")
	dSigCompositionHist[stackhistsname].Draw("nostackhistsame")
	dBkgCompositionHist[stackhistsname][1].Draw("histsame")
	hData.Draw("same p")
	c1.Update()
	fnew2.cd()
	c1.Write()
	c1.Print('resulthists/'+stackhistsname.replace('_','')+'.png')
	c1.Delete()
	hratio.Delete()
	

print 'test a'
	

print 'test b'
print 'just created', os.getcwd()+'/'+fnew2.GetName()
fnew2.Close()
print 'test c'
'''
	
	
