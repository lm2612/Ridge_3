import sys
home = os.getenv("HOME")
sys.path.insert(0, home+'/Ridge/UMDataModules/')
sys.path.insert(0, home+'/Ridge/Inputs/')
sys.path.insert(0, home+'/Ridge/PlotModules/')
sys.path.insert(0, home+'/Ridge/PredictionModules/')
from ImportData import *
from sklearn.preprocessing import scale
from sklearn.preprocessing import MinMaxScaler
from remove_ind import remove_ind
from SaveData import *
from remove_ind import *
import pickle
import multiprocessing as mp
import copy as cp
from Names import *
#Names,(X_SfcTemp,y)=remove_ind(Names,'No Dust Arabia',(X_SfcTemp,y))
# REMOVE ECLIPSE/MATTS/PDRMIP
#print Names
#for eclipse in eclipse_names:
#       (Names,[X_SfcTemp,X_GeoHeight500,X_RF,y]) = remove_ind(Names,eclipse,[X_SfcTemp,X_GeoHeight500,X_RF,y] )
#for pdrmip in pdrmip_names:
#        (Names,[X_SfcTemp,X_GeoHeight500,X_RF,y]) = remove_ind(Names,pdrmip,[X_SfcTemp,X_GeoHeight500,X_RF,y] )
#for matt in matt_names:
#       (Names,[X_SfcTemp,X_GeoHeight500,X_RF,y]) = remove_ind(Names,matt,[X_SfcTemp,X_GeoHeight500,X_RF,y] )
print(Names)

# What is the predictor X?
X = X_SfcTemp
X_name = 'SfcTemp'


Names,(X,y)=remove_ind(Names,'No Dust Arabia',(X_SfcTemp,y))
Names,(X,y)=remove_ind(Names,'',(X_SfcTemp,y))
Names,(X,y)=remove_ind(Names,'No Dust Arabia',(X_SfcTemp,y))
Names,(X,y)=remove_ind(Names,'No Dust Arabia',(X_SfcTemp,y))

# Any dimension reduction (eg PCA) or full grid?
X_type = 'PCA'
y_type = 'PCA'


# alpha for regularisation, no of CV
alpha_list = np.logspace(-3,8,10)
no_of_cv = 5

# where to save?
savedir = home+'/WORK/RemoveNoise/'
save_filename = 'X=SfcTemp_{},y={}_'.format(X_type,y_type)

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

