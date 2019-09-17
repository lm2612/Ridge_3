import sys
import os
home = os.getenv("HOME")
sys.path.insert(0, home+'/Ridge/UMDataModules/')
sys.path.insert(0, home+'/Ridge/Inputs/')
sys.path.insert(0, home+'/Ridge/PlotModules/')
sys.path.insert(0, home+'/Ridge/PredictionModules/')

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

directory = home+'/WORK/Full/plots/'
filestart = 'X=SfcTemp_Full,y=Full__'
Names = names[:]
regions_all = ['Global','Europe','China','East_Asia','India','Arctic',
              'US','South_America','Austrailia','Africa','NHML','NH']
regions_all = RegionsList

all_predictions = np.zeros((len(Names),192*145))
all_true = np.zeros((len(Names),192*145))


def run_one(directory,name,regions_all,i):
    # open file
    print(name)
    filename = directory+filestart+name+'_data' 
    d = pickle.load(open(filename,'rb') )
    print(d)
    print((d.y_pred-d.y_test))
    all_predictions[i,:]=d.y_pred.copy()
    all_true[i,:]=d.y_test.copy()
    

    

if __name__ == '__main__':
    # Define an output queue
    output = mp.Queue()

    # Loop over all predictions
    # Setup a list of processes that we want to run
    processes = [mp.Process(target=run_one, args=(directory,name,regions_all,i)) for (name,i) in zip(Names,list(range(len(Names))))]

    # Run processes
    for p in processes:
        p.start()

    # Exit the completed processes
    for p in processes:
        p.join()

    print('done')
    filename = directory+filestart+name+'_data'
    print((all_true-all_predictions))
    d = pickle.load(open(filename,'rb') )
    r2_err = r2_score(all_true, all_predictions, multioutput='raw_values')
    r2_err = np.reshape(r2_err,(145,192))
    print((r2_err))
    N = 26
    p = 145*192
    r2_adj = 1.-(1.-r2_err)*(N-1.)/(N-p-1.)
    r2_adj = r2_err- (1.-r2_err)*p/(N-p-1.)
    saveas = directory+'allruns_R2plot.png'
    plotmap(d.lons,d.lats,r2_err,savefile=saveas,levels=np.arange(0.5,1.04,0.01),
            cmap='Reds',plottitle='R2 error')
    saveas  = directory+'allruns_adjR2plot.png'
    plotmap(d.lons,d.lats,r2_adj,savefile=saveas,levels=np.arange(0.,1.04,0.01),
            cmap='Reds',plottitle='Adjusted R2 error')
    print('plots complete')
    # Get process results from the output queue
    #results = [output.get() for p in processes]

    #for result in results:
    #    print result + ' Done '

