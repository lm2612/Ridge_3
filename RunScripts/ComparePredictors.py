import sys
import os
home = os.getenv("HOME")
sys.path.insert(0, home+'/Ridge/UMDataModules/')
sys.path.insert(0, home+'/Ridge/Inputs/')
sys.path.insert(0, home+'/Ridge/PlotModules/')
sys.path.insert(0, home+'/Ridge/PredictionModules/')


from ImportData import *
from PredictionData import *
import numpy as np
from sklearn.preprocessing import scale
from sklearn.preprocessing import MinMaxScaler
from remove_ind import remove_ind
from SaveData import *
from remove_ind import *
import pickle
import multiprocessing as mp
import copy as cp
from Names import *


print(Names)
Noisy = ['No Dust Arabia','No VOC Global','No SO2 India','No OC Global','No NOX Global']
for runname in Noisy:
       (Names,[X_SfcTemp,X_GeoHeight500,X_RF,y]) = remove_ind(Names,runname,[X_SfcTemp,X_GeoHeight500,X_RF,y] )
# What is the predictor X?
X = X_GeoHeight500
X_name = 'GeoHeight500'


# Any dimension reduction (eg PCA) or full grid?
X_type = 'Full'
y_type = 'Full'


# alpha for regularisation, no of CV
alpha_list = np.logspace(-3,8,10)
no_of_cv = 3

# where to save?
savedir = home+'/OutputsRidge/'
save_filename = 'X={}_{},y={}_'.format(X_name,X_type,y_type)

# regions of interest for metrics?
from RegionLatitudes  import *
#regions_all = ['Global','Europe','US','China','East_Asia','India','NHML','Tropics','Africa','South_America','SHML','Arctic','Austrailia','NH','Tropics','SHML']
regions_all = ['Global']+RegionsList
d = PredictionData(X,y,Names,lons,lats,lons1,lats1)
d.setup(X_type,y_type)

d.save_X()

def run_one(data,name,output):
    # make a copy so we don't overwrite
    d = cp.copy(data)
    d.re_initialise()
    d.run(X_type,y_type,'Ridge',name,cvfolds=no_of_cv,alpha_list=alpha_list, coefs=True, repeat_regularise=True, n_jobs=4)
    saveas = savedir+save_filename+name+'_'
    d.metrics_regional(saveas,regions_all)
    d.plot_results(savedir)
    d.pickle_object(savedir+'PickledData_%s_%s'%(save_filename,name))

if __name__ == '__main__':
    # Define an output queue
    output = mp.Queue()

    # Loop over all predictions
    # Setup a list of processes that we want to run
    processes = [mp.Process(target=run_one, args=(d,name,output)) for name in Names]

    # Run processes
    for p in processes:
        p.start()

    # Exit the completed processes
    for p in processes:
        p.join()

    print('done')

