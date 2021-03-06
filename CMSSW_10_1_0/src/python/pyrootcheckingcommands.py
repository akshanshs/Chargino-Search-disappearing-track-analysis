from ROOT import *
from utilitiesII import *
h = TH1F('h1','',10,-3,3)

h.FillRandom('gaus',1000)

h.Draw("hist e")

pause()

hvariation1 = h.Clone('hvariation1')
xax = hvariation1.GetXaxis()
for ibin in range(1,xax.GetNbins()+1):
    print ibin, hvariation1.GetBinContent(ibin)

pause()

print 'a = np.random.poisson(5, 10000)'

a = np.random.poisson(20.5, 15)

print 'a[0]', a[0]
print 'a[1]', a[1]

print 'printing full array a', a

pause()

print 'a = np.random.poisson(5)'
a = np.random.poisson(10)
print a
pause()

print 'a = np.random.poisson(5)'
a = np.random.poisson(1)
print a
pause()

print 'a = np.random.poisson(5)'
a = np.random.poisson(.1)
print a
pause()

print 'a = np.random.poisson(5)'
a = np.random.poisson(.01)
print a
pause()

print 'going back to the gaus hinto grams, printing values in 10 bin histogram'

for ibin in range(1,xax.GetNbins()+1):
    print ibin, hvariation1.GetBinContent(ibin)

pause()

print 'going to variate the distribution'

for ibin in range(1,xax.GetNbins()+1):
    newcontent=np.random.poisson(hvariation1.GetBinContent(ibin))
    hvariation1.SetBinContent(ibin, newcontent)

print 'will overlay one variation ' 
h.Draw("hist e")
hvariation1.Draw("histsame e")

pause()

print 'going to do secomd variation'

hvariation2 = h.Clone('hvariation2')
xax = hvariation2.GetXaxis()

for ibin in range(1,xax.GetNbins()+1):
    newcontent=np.random.poisson(hvariation2.GetBinContent(ibin))
    hvariation2.SetBinContent(ibin, newcontent)

h.Draw("hist e")
hvariation1.Draw("histsame e")
hvariation2.Draw("histsame e")

pause()
