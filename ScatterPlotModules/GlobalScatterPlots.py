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
time=1
from ReadAvgFiletyr import *
from ScatterPlot import *
from ReadRegions import *
from RegionalInputs import *
plt.clf()
fig = plt.figure(figsize=(10,8))
ax1 = plt.subplot2grid((2, 3), (0, 0))
ax2 = plt.subplot2grid((2, 3), (0, 1))
ax3 = plt.subplot2grid((2, 3), (0, 2))
ax4 = plt.subplot2grid((2, 3), (1, 0))
ax5 = plt.subplot2grid((2, 3), (1, 1))
ax6 = plt.subplot2grid((2, 3), (1, 2))

axes = [ax1,ax2,ax3,ax4,ax5,ax6]

(X_SfcTemp,X_AirTemp500,X_GeoHeight500,X_SLP,X_RF,y,
                nlon,nlat,lons,lons1,lats,lats1,Files,Names) = OpenFile(time)
N,p = X_SfcTemp.shape

colors = cm.rainbow(np.linspace(0, 1, N))
print(colors)
print(y.shape,X_SfcTemp.shape)

plt.rc('text', usetex=True)
font = {'family' : 'normal', 'size' : 10} 
plt.rc('font',**font)

area = Area(lons1,lats1).flatten()
times= [1,2,3,4,5]
for i in range(len(times)):
	time = times[i]
	(X_SfcTemp,X_AirTemp500,X_GeoHeight500,X_SLP,X_RF,y,
                nlon,nlat,lons,lons1,lats,lats1,Files,Names) = OpenFile(time)		
	Tmean = np.average(X_SfcTemp,axis=1,weights=area)
	ymean = np.average(y,axis=1,weights=area)
	ax = axes[i]
	ax=Scatter(Tmean,ymean,ax,title='',xlabel='Global mean $\Delta T_{%s yr}$'%time,ylabel='Global mean $\Delta T_{eq}$ ',ymax=7.,xmax=3.)


from ReadAvgFile import *
time=10
ax = ax6
Tmean = np.average(X_SfcTemp,axis=1,weights=area)
ymean = np.average(y,axis=1,weights=area)
ax=Scatter(Tmean,ymean,ax,title='',xlabel='Global mean $\Delta T_{%s yr}$'%time,ylabel='Global mean $\Delta T_{eq}$ ',ymax=7.,xmax=7.)
	
plt.tight_layout()
plt.savefig('/Users/lm2612/Documents/PhD/plots/Scatters/AllRegions/%s_year_globalmean.png'%(time))
