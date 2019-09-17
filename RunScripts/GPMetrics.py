import sys
sys.path.insert(0, '/home/lm2612/Ridge/UMDataModules/')
sys.path.insert(0, '/home/lm2612/Ridge/Inputs/')
sys.path.insert(0, '/home/lm2612/Ridge/PlotModules/')
sys.path.insert(0, '/home/lm2612/Ridge/PredictionModules/')

from Metrics import *
from sklearn.preprocessing import scale
from sklearn.preprocessing import MinMaxScaler
from SaveData import *
import multiprocessing as mp
import copy as cp
from Names import *
import pickle as pickle
from RegionLatitudes import *

directory = '/work/lm2612/GP/'
Names = names[:]
regions_all = ['Global','Europe','China','East_Asia','India','Arctic',
              'US','South_America','Austrailia','Africa','NHML','NH']
regions_all = RegionsList
def run_one(directory,name,regions_all):
    # open file
    filename = directory+name+'_output2' 
    data = pickle.load(open(filename,'rb'))
    saveas = directory+name+'_newmetrics'
    RegionalMetrics(data['y_pred'],data['y_test'],regions_all,data['lons'],data['lats'],
                 data['lons1'],data['lats1'], data['names_train'], data['names_test'],saveas,data['area_flat'])


if __name__ == '__main__':
    # Define an output queue
    output = mp.Queue()

    # Loop over all predictions
    # Setup a list of processes that we want to run
    processes = [mp.Process(target=run_one, args=(directory,name,regions_all)) for name in Names]

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

