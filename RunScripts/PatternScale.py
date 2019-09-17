import sys
import os
home = os.getenv("HOME")
sys.path.insert(0, home+'/Ridge/UMDataModules/')
sys.path.insert(0, home+'/Ridge/Inputs/')
sys.path.insert(0, home+'/Ridge/PlotModules/')
sys.path.insert(0, home+'/Ridge/PredictionModules/')
from ImportData import *
from PredictionData import *
from sklearn.preprocessing import scale
from sklearn.preprocessing import MinMaxScaler
from remove_ind import remove_ind
from SaveData import *
from remove_ind import *
import pickle
import multiprocessing as mp
import copy as cp
from Names import *
import numpy as np
from GetDir import *
from ReadAvgFiletyr import *

datadir = GetDir()
time = 5
print(Names)
X = X_RF
CO2_ind =(Names.index('2X CO2'))
CO2_change = y[CO2_ind]
CO2_RF = X_RF[CO2_ind]

print(CO2_change.shape)
area_flat = Area(lons1,lats1).flatten()
CO2_pattern = CO2_change/(np.sum(CO2_RF))
y_pred = np.zeros(y.shape)
print((y_pred.shape))
for i in range(len(Names)):
    print((Names[i]))
    RF = X_RF[i]
    predicted = CO2_pattern*np.sum(RF)
    y_pred[i,:] = predicted

print(y_pred)
y_test = y

savedir = home+'/WORK/PatternScale/'
save_filename = 'Matt'

# regions of interest for metrics?
regions_all = RegionsList 

X_type = 'Full'
y_type= 'Full'
data = PredictionData(X,y,Names,lons,lats,lons1,lats1)
data.setup(X_type,y_type)


for i in range(len(Names)):
    # make a copy so we don't overwrite
    d = cp.copy(data)
    d.re_initialise()
    name = Names[i] 
    d.split_set(Names[i])
    d.y_pred = (np.reshape(y_pred[i],(1,-1)))
    
    saveas = savedir+save_filename+name+'_'
    d.metrics_regional(saveas,regions_all)
    d.plot_results(savedir+'plots/')
    d.pickle_object(savedir+'plots/%s_%s_data'%(save_filename,name))

