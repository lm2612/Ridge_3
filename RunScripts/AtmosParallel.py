import sys
sys.path.insert(0, '/home/lm2612/Ridge/UMDataModules/')
sys.path.insert(0, '/home/lm2612/Ridge/Inputs/')
sys.path.insert(0, '/home/lm2612/Ridge/PlotModules/')
sys.path.insert(0, '/home/lm2612/Ridge/PredictionModules/')


from ImportData import *
from RegionalDimReduction import split_into_regions

# Import Atmos only data
(X_SfcTemp_Atm,X_AirTemp500_Atm,X_GeoHeight500_Atm,X_SLP_Atm,X_RF_Atm,y_Atm,
                lons,lats,lons1,lats1,Names_Atm) = OpenFile(datadir+'Atmos_15yr.nc',
['SfcTemp_1','AirTemp_1','GeoHeight_1','SLP_1',
                      'RF_1','SfcTempResponse_1'])

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

print(Names)

# What is the predictor X?
X = X_SfcTemp_Atm
X_name = 'SfcTemp'

# Any dimension reduction (eg PCA) or full grid?
X_type = 'Full'
y_type = 'Full'


# alpha for regularisation, no of CV
alpha_list = np.logspace(-3,8,10)
no_of_cv = 5

# where to save?
savedir = '/work/lm2612/AtmOnlyPCA/'
save_filename = 'X=SfcTemp_PCA,y=PCA_'

# regions of interest for metrics?
regions_all = ['Global','Europe','Sahel','US','China','East_Asia','India','NHML','Tropics','Africa','South_America','SHML','Arctic','Austrailia','NH','Tropics','SHML']


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

