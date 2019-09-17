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
import matplotlib.pyplot as plt
from plotmapfunction import *
Noisy = ['No Dust Arabia','No VOC Global','No SO2 India','No OC Global','No NOX Global']
for runname in Noisy:
       (Names,[X_SfcTemp,X_GeoHeight500,X_RF,y]) = remove_ind(Names,runname,[X_SfcTemp,X_GeoHeight500,X_RF,y] )

newXy,newlons,newlats = ReduceRes([X_SfcTemp,y],lons,lats,factor_lat=8,factor_lon=8) 
Xnew = newXy[0]
ynew = newXy[1]
print((newlons,newlats))
print((newlons.shape,newlats.shape,Xnew.shape))
lons = newlons
lats = newlats
y = ynew
nlat1 = len(newlats)-1
nlon1 = len(newlons)
lats1 = np.zeros(nlat1)
lons1 = newlons
for i in range(nlat1):
    lats1[i] = (newlats[i]+newlats[i+1])/2.
print(lats1)


# What is the predictor X?
X = Xnew
X_name = 'SfcTemp'

print((X_SfcTemp.shape))
print((y.shape))
print(lons)
print(lats)
nlat = len(lats)
nlon = len(lons)
# Any dimension reduction (eg PCA) or full grid?
X_type = 'Full'
y_type = 'Full'


# alpha for regularisation, no of CV
alpha_list = np.logspace(-2,5,10)
no_of_cv = 5

# where to save?
savedir = '/rds/general/user/lm2612/home/WORK/LowLowResNew/'
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
