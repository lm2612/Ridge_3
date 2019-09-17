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
X = X_SfcTemp
X_name = 'SfcTemp'


# Any dimension reduction (eg PCA) or full grid?
X_type = 'Full'
y_type = 'Full'


# alpha for regularisation, no of CV
alpha_list = np.logspace(-3,8,10)
no_of_cv = 5

# where to save?
savedir = home+'/WORK/RemoveNoiseNew_withcoefs/'
save_filename = 'X=SfcTemp_{},y={}_'.format(X_type,y_type)

# regions of interest for metrics?
from RegionLatitudes  import *
#regions_all = ['Global','Europe','US','China','East_Asia','India','NHML','Tropics','Africa','South_America','SHML','Arctic','Austrailia','NH','Tropics','SHML']
regions_all = ['Global']+RegionsList
d = PredictionData(X,y,Names,lons,lats,lons1,lats1)
d.setup(X_type,y_type)

d.save_X()
alphas = {'10X Asia BC': 3.874204890000002e-05,
 '10X Asia SO4': 12064.203361878084,
 '10X BC': 1818.774758136308,
 '10X CFC-12': 2875.2023514253383,
 '10X Europe SO4': 3741.876533459929,
 '2% Solar Constant increase': 5702.7047354700435,
 '2X CO2': 418.3946300353087,
 '2xCO2 Global': 3.874204890000002e-05,
 '3X CH4': 1391.7276253324446,
 '5X SO4': 1054.8229344131157,
 'No BC Global': 5327.931926128546,
 'No BC NHML': 5375.19181764409,
 'No CH4 Global': 3.874204890000002e-05,
 'No CO Global': 3.874204890000002e-05,
 'No SO2 China': 5612.218363130979,
 'No SO2 East Asia': 4539.33861771818,
 'No SO2 Europe': 3588.341442413211,
 'No SO2 Global': 3.874204890000002e-05,
 'No SO2 NHML': 6693.4443757368,
 'No SO2 US': 4070.0764829237996,
 'pre-industrial SO4': 4525.537723373411}

def run_one(data,name,output):
    # make a copy so we don't overwrite
    d = cp.copy(data)
    d.re_initialise()
    d.run(X_type,y_type,'Ridge',name,cvfolds=no_of_cv,alpha_list = [alphas[name]], coefs=True, repeat_regularise=False)
    saveas = savedir+save_filename+name+'_'
    d.metrics_regional(saveas,regions_all)
    d.plot_results(savedir+'plots/')
    d.pickle_object(savedir+'plots/%s_%s_data_withcoefs'%(save_filename,name))
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

