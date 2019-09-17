import sys
sys.path.insert(0, '../UMDataModules/')
sys.path.insert(0, '../Inputs/')
sys.path.insert(0, '../PlotModules/')
sys.path.insert(0, '../PredictionModules/')
from ImportData import *
from remove_ind import remove_ind
from plotmapfunction import *
from PredictionData import *
# What is the predictor X?
X = X_SfcTemp
X_name = 'SfcTemp'

# where to save?
savedir = '/rds/general/user/lm2612/home/WORK/R2plots/'

N,p = y.shape
nlat,nlon = len(lats),len(lons)

import pickle
from PredictionData import *
directory = '/work/lm2612/EvenlyWeightedGrid/plots/X=SfcTemp_Full,y=Full__'
Names = names[:]
regions_all = ['Global','Europe','China','East_Asia','India','Arctic',
              'US','South_America','Austrailia','Africa','NHML','NH']
regions_all = RegionsList
def run_one(directory,name,regions_all):
    # open file
    filename = directory+name+'_data'
    d = pickle.load(open(filename,'rb') )
    print(d)

for i in range(1):
    inp = X[:,i]
    # what lon and lat?
    lon_ind = int(i/nlon)
    lat_ind = i%nlon
    lon = lons[lon_ind]
    lat = lats[lat_ind]
    emptyarr = np.zeros(p)
    emptyarr[i] = 1.0
    R2 = np.zeros(p)
    for j in range(p):
        outp = y[:,j]
        mean_y = np.mean(outp)
        SSR = np.mean( (outp-mean_y)**2. )
    R2map = np.reshape(R2,(nlat,nlon))
    plt.clf()
    print(R2map)
    plotmap(lons,lats,R2map,levels = np.arange(0.,1.05,0.05))
    plt.gca()
    if lon>360.:
        lon = lon-360.
    plt.plot(lon,lat,'kx')
    plt.savefig(savedir+'map_lon{}_lat{}.png'.format(lon,lat))
