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
RF_file = 'All_Atmos_incRF_-1yr.nc'
filename = datadir+RF_file
(X_RF,lons,lats,lons1,lats1,Names_Atm) = OpenFile(filename,['RF_1'])

print(Names_Atm)
# Put in same order
N_atm = len(Names_Atm)
N_cpl,p = y.shape
print("N_cpl %s, N_atm %s, "%(N_cpl,N_atm))
new_y = np.zeros((N_atm,p))

for atm_ind in range(N_atm):
        name = Names_Atm[atm_ind]
        print(atm_ind,name)

        cpl_ind = Names.index(name)
        print(cpl_ind)
        new_y[atm_ind,:] = y[cpl_ind,:]
y = new_y.copy()

Names = Names_Atm

print(Names)
Noisy = ['No SO2 India','No OC Global']
for runname in Noisy:
       (Names,[X_RF,y]) = remove_ind(Names,runname,[X_RF,y] )

# REMOVE ECLIPSE/MATTS/PDRMIP
print(Names)

# What is the predictor X?
X = X_RF
X_name = 'RF'

# Any dimension reduction eg pca or full grid?
X_type = 'Full'
y_type = 'Full'


# alpha for regularisation, no of CV
alpha_list = np.logspace(-3,8,10)
no_of_cv = 5

# where to save?
savedir = home+'/WORK/RFfSST/'
save_filename = 'X=SfcTemp_{},y={}_'.format(X_type,y_type)

# regions of interest for metrics?
regions_all = RegionsList 


d = PredictionData(X,y,Names,lons,lats,lons1,lats1)
d.setup(X_type,y_type)

d.save_X()


def run_one(data,name,output):
    # make a copy so we don't overwrite
    d = cp.copy(data)
    d.re_initialise()
    d.run(X_type,y_type,'Ridge',name,cvfolds=no_of_cv,alpha_list = alpha_list)
    saveas = savedir+save_filename+name+'_'
    d.metrics_regional(saveas,regions_all)
    d.plot_results(savedir+'plots/')
    d.pickle_object(savedir+'plots/%s_%s_data'%(save_filename,name))
    #output.put((name))

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
    # Get process results from the output queue
    #results = [output.get() for p in processes]

    #for result in results:
    #    print result + ' Done '

