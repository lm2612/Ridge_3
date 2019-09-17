import sys
sys.path.insert(0, '/home/lm2612/Ridge/UMDataModules/')
sys.path.insert(0, '/home/lm2612/Ridge/Inputs/')
sys.path.insert(0, '/home/lm2612/Ridge/PlotModules/')
sys.path.insert(0, '/home/lm2612/Ridge/PredictionModules/')

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
from DummyRegressor import *
print(Names)

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
savedir = '/work/lm2612/DummyRegressor/'
save_filename = 'X=SfcTemp_Full,y=Full_'

# regions of interest for metrics?
regions_all = ['Global','Europe','Sahel','US','China','East_Asia','India','NHML','Tropics','Africa','South_America','SHML','Arctic','Austrailia','NH','Tropics','SHML']


def run_one(name,output,X,y,names,lons,lats,lons1,lats1):
    d = AllDummyPrediction(name,X,y,names,lons,lats,lons1,lats1)
    saveas = savedir+save_filename+name+'_'
    d.metrics_regional(saveas,regions_all)
    d.plot_results(savedir+'plots/')
    d.pickle_object(savedir+'plots/%s_%s_data'%(save_filename,name))


if __name__ == '__main__':
    # Define an output queue
    output = mp.Queue()

    # Loop over all predictions
    # Setup a list of processes that we want to run
    processes = [mp.Process(target=run_one, args=(name,output,X,y,names,lons,lats,lons1,lats1)) for name in Names]

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

