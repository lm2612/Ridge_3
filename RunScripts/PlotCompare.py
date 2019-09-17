import sys
sys.path.insert(0, '../UMDataModules/')
sys.path.insert(0, '../Inputs/')
sys.path.insert(0, '../PlotModules/')

import numpy as np
import matplotlib.cm as cm
from plotmapfunction import *

def plot_compare(lons,lats,y1,y2,y3,y4,y5,runname,savefolder,titles=['']*5):
    plt.clf()
    fig = plt.figure(figsize=(15,15))
    ax2 = plt.subplot2grid((3, 2), (0, 0),rowspan=1,colspan=2)
    ax3 = plt.subplot2grid((3, 2), (1, 0))
    ax4 = plt.subplot2grid((3, 2), (1, 1))
    ax5 = plt.subplot2grid((3, 2), (2, 0))
    ax6 = plt.subplot2grid((3, 2), (2, 1))

    maxlvl = np.ceil(np.max(np.abs(y1))*0.8)
    levels = np.arange(-maxlvl,maxlvl+0.01,maxlvl/50.)
    plt.sca(ax2)
    plotmap(lons,lats,y1,cmap='RdBu_r',
                levels=levels,plottitle=titles[0],
                plotaxis=ax2)

    plt.sca(ax3)
    plotmap(lons,lats,y2,cmap='RdBu_r',levels=levels,plottitle=titles[1],
                        plotaxis=ax3,colorbar=0)

    plt.sca(ax4)
    plotmap(lons,lats,y3,cmap='RdBu_r',levels=levels,plottitle=titles[2],
                        plotaxis=ax4,colorbar=0)

    plt.sca(ax5)
    plotmap(lons,lats,y4,cmap = 'RdBu_r',plottitle=titles[3],
                        levels=levels,plotaxis=ax5,colorbar=0)

    plt.sca(ax6)
    plotmap(lons,lats,y5,cmap = 'RdBu_r',plottitle=titles[4],
                        levels=levels,plotaxis=ax6,colorbar=0)
    #fig.suptitle(runname)
    savefileas = savefolder+'%s_compare.png'%(runname.replace(' ','_'))
    plt.savefig(savefileas,bbox_inches='tight')
    print("Saved as ",savefileas)
    plt.close()
