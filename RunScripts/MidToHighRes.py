import glob 
import sys
sys.path.insert(0, '../UMDataModules/')
sys.path.insert(0, '../Inputs/')
sys.path.insert(0, '../PlotModules/')
sys.path.insert(0, '../PredictionModules/')
from ImportData import *
from remove_ind import remove_ind
from plotmapfunction import *
from PredictionData import *
from Regrid import *


X = X_SfcTemp
X_name = 'SfcTemp'

# where to save?
savedir = '/rds/general/user/lm2612/home/WORK/MidRes/'
filenames = glob.glob(savedir+'/plots/*data')
N,p = y.shape
nlat,nlon = len(lats),len(lons)

import pickle
from PredictionData import *

regions_all = RegionsList


d0 = PredictionData(X,y,Names,lons,lats,lons1,lats1)
d0.setup('Full','Full')


def run_one(directory,regions_all):
    # open file
    d = pickle.load(open(filename,'rb'))
    print(d)
    newXy,newlons,newlats = ReduceRes([d.y_test,d.y_pred],d.lons,d.lats,nlat=nlat,nlon=nlon)
    print((newlats.shape,lats.shape))
    d.lons = lons
    d.lats = lats
    d.lats1 = lats1
    d.lons1 = lons1
    d.area_X = d0.area_X
    d.area_y = d0.area_y
    d.y_test = newXy[0]
    d.y_pred = newXy[1]
    saveas = filename+'high_res'
    d.metrics_regional(saveas,regions_all)
    d.plot_results(savedir+'plots/')
    d.pickle_object(filename+'high_res')

for filename in filenames:
    run_one(filename,regions_all)

