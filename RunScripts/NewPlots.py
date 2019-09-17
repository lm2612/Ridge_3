import sys
sys.path.insert(0, '../UMDataModules/')
sys.path.insert(0, '../Inputs/')
sys.path.insert(0, '../PlotModules/')
sys.path.insert(0, '../PredictionModules/')

from PredictionData import *
from sklearn.preprocessing import scale
from sklearn.preprocessing import MinMaxScaler
from SaveData import *
import multiprocessing as mp
import copy as cp
from Names import *
import pickle
from RegionLatitudes import *
from PlotCompare import *
home_directory = '/rds/general/user/lm2612/home/'
plot_to = home_directory+'CompareMethodsPlots/'
filedirectory_names = ['RemoveNoiseNew','LassoNew','GPRemoveNoise','PatternScale']
file_directory =[ home_directory+'WORK/'+dirname+'/plots/' for dirname in filedirectory_names]
file_start = ['X=SfcTemp_Full,y=Full__','X=SfcTemp_Full,y=Full__','','PatternScale_']
file_end = ['_data','_data','_output2','_data']
methods = ['Ridge','Lasso','GP','PatternScale']
titles = ['True','Ridge','Lasso','Gaussian Process','Pattern Scaling']
Names = names[:]


nlat = 145
nlon = 192
flag = True
for name in Names:
    ys = []
    for i in range(0,4):
        filename = file_directory[i]+file_start[i]+name+file_end[i]
        print(filename)
        try:
            d = pickle.load(open(filename,'rb')) 
        except IOError as e:
            print(e)
            flag=False
            continue
            
        if i==0:
            ys.append(d.y_test.reshape((nlat,nlon)))
            lons = d.lons
            lats = d.lats
            print(lons)
        if i==2:
            ys.append(d['y_pred'].reshape((nlat,nlon)))
        else:
            ys.append(d.y_pred.reshape((nlat,nlon)))
    if flag:
        plot_compare(lons,lats,ys[0],ys[1],ys[2],ys[3],ys[4],name,plot_to,titles=titles)

    else: 
        flag = True
