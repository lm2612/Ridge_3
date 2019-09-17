import sys
sys.path.insert(0, '/home/lm2612/Ridge/UMDataModules/')
sys.path.insert(0, '/home/lm2612/Ridge/Inputs/')
sys.path.insert(0, '/home/lm2612/Ridge/PlotModules/')
sys.path.insert(0, '/home/lm2612/Ridge/PredictionModules/')


from ImportData import *
from Regrid import *
from PredictionData import *
from sklearn.preprocessing import scale
from sklearn.preprocessing import MinMaxScaler
from remove_ind import remove_ind
from SaveData import *
from remove_ind import *
import multiprocessing as mp
import copy as cp
from Names import *
# Regrid onto smaller grid: 1/4 of the size
nlon = int(len(lons)/8)
nlat = int(len(lats)/5)
p = nlon*nlat
# keep min and max of current lons and lats, linearly space
newlons = np.linspace(np.min(lons),np.max(lons),nlon)
newlats = np.linspace(np.min(lats),np.max(lats),nlat)

nlat1 = len(newlats)-1
nlon1 = len(newlons)
lats1 = np.zeros(nlat1)
lons1 = newlons 
for i in range(nlat1):
    lats1[i] = (newlats[i]+newlats[i+1])/2.
print(lats1)

# Need to grid it for each sample
N = X_SfcTemp.shape[0]
Xnew = np.zeros((N,p))
ynew = np.zeros((N,p))
for i in range(N):
    X = np.reshape(X_SfcTemp[i,:],(len(lats),len(lons)))
    X_regridded = Regridder(X,lons,lats,newlons,newlats)
    print((X_regridded.shape))
    X_flat = X_regridded.flatten()
    Xnew[i,:] = X_flat

    yi = np.reshape(y[i,:],(len(lats),len(lons)))
    y_regridded = Regridder(yi,lons,lats,newlons,newlats)
    print((y_regridded.shape))
    y_flat = y_regridded.flatten()
    ynew[i,:] = y_flat

print((newlons,newlats))
print((newlons.shape,newlats.shape,Xnew.shape))
lons = newlons
lats = newlats
y = ynew

# What is the predictor X?
X = Xnew
X_name = 'SfcTemp'

# Any dimension reduction (eg PCA) or full grid?
X_type = 'PCA'
y_type = 'PCA'


# alpha for regularisation, no of CV
alpha_list = np.logspace(-2,5,10)
no_of_cv = 5

# where to save?
savedir = '/work/lm2612/VeryCoarseGrid/'
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

