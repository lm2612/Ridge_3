from ImportData import *
from PredictionData import *
from sklearn.preprocessing import scale
from sklearn.preprocessing import MinMaxScaler
from remove_ind import remove_ind
from SaveData import *
from remove_ind import *
import multiprocessing as mp
import copy as cp
#Names,(X_SfcTemp,y)=remove_ind(Names,'No Dust Arabia',(X_SfcTemp,y))
print(Names)

# What is the predictor X?
X = X_SfcTemp
X_name = 'SfcTemp'

# Scaling
def scalex(x):
    xnew = (x - np.min(x))/(np.max(x)-np.min(x))
    return xnew

for i in range(len(Names)):
    X_SfcTemp[i,:] = scalex(X_SfcTemp[i,:])
    y[i,:] = scalex(y[i,:])

# remove CO2 pattern
CO2_ind = Names.index('2xCO2 Global')
print(CO2_ind)
Temp_CO2 = X_SfcTemp[CO2_ind,:]
y_CO2 = y[CO2_ind,:]
for i in range(len(Names)):
    X_SfcTemp[i,:] = X_SfcTemp[i,:] - Temp_CO2
    y[i,:] = y[i,:] - y_CO2



# Any dimension reduction (eg PCA) or full grid?
X_type = 'PCA'
y_type = 'PCA'


# alpha for regularisation, no of CV
alpha_list = np.logspace(-1,5,300)
no_of_cv = 5

# where to save?
savedir = '/home/lm2612/plots/RemoveCO2/'
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

