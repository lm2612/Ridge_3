# SpatialTest.py
# Fri 2 Feb 11:15 
#
# lm2612
#

# Import packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as mpatches
from ReadAvgFiletyr import *
from ScatterPlot import *
from ReadRegions import *
from RegionalInputs import *
plt.clf()
fig = plt.figure(figsize=(10,8))
ax1 = plt.subplot2grid((2, 4), (0, 0))
ax2 = plt.subplot2grid((2, 4), (0, 1))
ax3 = plt.subplot2grid((2, 4), (0, 2))
ax4 = plt.subplot2grid((2, 4), (0, 3))
ax5 = plt.subplot2grid((2, 4), (1, 0))
ax6 = plt.subplot2grid((2, 4), (1, 1))
ax7 = plt.subplot2grid((2, 4), (1, 2))
ax8 = plt.subplot2grid((2, 4), (1, 3))

axes = [ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8]

time=1
(X_SfcTemp,X_AirTemp500,X_GeoHeight500,X_SLP,X_RF,y,
                nlon,nlat,lons,lons1,lats,lats1,Files,Names) = OpenFile(time)
#from ReadAvgFile import *
N,p = X_SfcTemp.shape

colors = cm.rainbow(np.linspace(0, 1, N))
print(colors)
print(y.shape,X_SfcTemp.shape)
Regions = ['NHML','US','Europe','East_Asia','China','India','Africa','South_America']
X_reg = RegionalInputs(X_SfcTemp,lons1,lats1,Regions)
y_reg = RegionalInputs(y,lons1,lats1,Regions)
print(X_reg.shape)

plt.rc('text', usetex=True)
font = {'family' : 'normal', 'size' : 10} 
plt.rc('font',**font)
for i in range(len(Regions)):
	plt.clf()
	fig = plt.figure(figsize=(10,6))
	ax1 = plt.subplot2grid((2, 4), (0, 0))
	ax2 = plt.subplot2grid((2, 4), (0, 1))
	ax3 = plt.subplot2grid((2, 4), (0, 2))
	ax4 = plt.subplot2grid((2, 4), (0, 3))
	ax5 = plt.subplot2grid((2, 4), (1, 0))
	ax6 = plt.subplot2grid((2, 4), (1, 1))
	ax7 = plt.subplot2grid((2, 4), (1, 2))
	ax8 = plt.subplot2grid((2, 4), (1, 3))

	axes = [ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8]
	
	region = Regions[i]
	print(region)
	title=Regions[i].replace('_',' ')
	print(len(X_reg[i]))
	for j in range(len(Regions)):
		Scatter(X_reg[:,i],y_reg[:,j],ax = axes[j],title=title,ylabel='$\Delta T_{eq}$ in %s'%title,xlabel='$\Delta T_{init}$ in %s'%Regions[j].replace('_',' '))
	
	plt.tight_layout()
	plt.savefig('/Users/lm2612/Documents/PhD/plots/Scatters/AllRegions/%s_year_%s_all.png'%(time,region))
