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
from sklearn.metrics import r2_score
from plotmapfunction import *

savedir = '/general/user/lm2612/home/WORK/R2plots/'
directory = '/rds/general/user/lm2612/home/WORK/Full/plots/'
filestart = 'X=SfcTemp_Full,y=Full__'
Names = names[:]
regions_all = ['Global','Europe','China','East_Asia','India','Arctic',
              'US','South_America','Austrailia','Africa','NHML','NH']
regions_all = RegionsList

all_predictions = np.zeros((len(Names),192*145))

def run_one(directory,name,regions_all):
    # open file
    filename = directory+filestart+name+'_data' 
    d = pickle.load(open(filename,'rb') )
    print(d)
    saveas = directory+name+'_R2plots_training'
    print((d.y_test,d.y_pred))
    print((d.y_test.shape,d.y_pred.shape))
    r2_err = r2_score(d.X_train, d.y_train, multioutput='raw_values')
    r2_err = np.reshape(r2_err,(len(d.lats),len(d.lons)))
    print((r2_err))
    plotmap(d.lons,d.lats,r2_err,savefile=saveas,levels=np.arange(-1.,1.04,0.05),
            plottitle='R2 error')
     
    
    

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

