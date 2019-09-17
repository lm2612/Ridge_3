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
from PredictionData import *
from sklearn.preprocessing import scale
from sklearn.preprocessing import MinMaxScaler
from SaveData import *
import multiprocessing as mp
import copy as cp
from Names import *
import pickle
from RegionLatitudes import *

directory = '/rds/general/user/lm2612/home/WORK/Full/plots/'
filestart = 'X=SfcTemp_Full,y=Full__'
Names = names[:]
regions_all = ['Global','Europe','China','East_Asia','India','Arctic',
              'US','South_America','Austrailia','Africa','NHML','NH']
regions_all = RegionsList
N = 25
p = 145*192
def run_one(directory,name,regions_all):
    # open file
    filename = directory+filestart+name+'_data' 
    d = pickle.load(open(filename,'rb') )
    print(d)
    ypr = d.y_pred.flatten()
    yt = d.y_test.flatten()
    plt.plot(yt,ypr,'k.')
    plt.xlabel('y true')
    plt.ylabel('y pred')
    plt.savefig(directory+'y-yplot_'+name+'.png')
    

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

