import sys
import os
home = os.getenv("HOME")
sys.path.insert(0, home+'/Ridge/UMDataModules/')
sys.path.insert(0, home+'/Ridge/Inputs/')
sys.path.insert(0, home+'/Ridge/PlotModules/')
sys.path.insert(0, home+'/Ridge/PredictionModules/')

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

from Names import *
from PredictionData import *
from sklearn.preprocessing import scale
from sklearn.preprocessing import MinMaxScaler
from SaveData import *
import multiprocessing as mp
import copy as cp
import pickle
from RegionLatitudes import *
from sklearn.metrics import r2_score
from plotmapfunction import *

directory = '/rds/general/user/lm2612/home/WORK/Full/plots/'
filestart = 'X=SfcTemp_Full,y=Full__'
Names = names[:]
regions_all = ['Global','Europe','China','East_Asia','India','Arctic',
              'US','South_America','Austrailia','Africa','NHML','NH']
regions_all = RegionsList


name = names[0]
filename = directory+filestart+name+'_data' 
d = pickle.load(open(filename,'rb') )
print(d)
names = d.names
y = d.y

nlon = 192
nlat =145
def plot_one(yi,name):
    saveas = directory+'RMSE_if_shifted'+name
    y_true = np.reshape(yi,(1,nlat,nlon))
    y_pred = np.zeros((1,nlat,nlon))
    y_pred[:,:,1:] = y_true[:,:,:-1]
    y_pred[:,:,0:1] = y_true[:,:,-1:]
    d.y_pred = np.reshape(y_pred,(1,-1))
    d.y_true = np.reshape(y_true,(1,-1))
    d.metrics_regional(saveas,regions_all)
    return(d)
  
processes = [plot_one(y[i],name) for (name,i) in zip(Names,list(range(len(Names))))]

