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
    alpha = d.alpha_params['alpha']
    y_pred,coef=Regression(d.X_train,d.y_train,d.X_test,d.y_test,reg_type='Ridge',coefs=True,alpha_list = [alpha],cvfolds=5)
    print(coef)
    BX = np.dot(d.X_train,coef)
    residuals = BX - d.y_train
    newfilename = directory+filestart+name+'_coefficients'

    #pickle.dump((coef,residuals),open(newfilename,'wb'))
    plt.hist(residuals,30)
    plt.title('Residuals')
    plt.savefig(directory+'residual_histogram'+name+'.png')
    plt.clf()
    plt.contourf(coef,cmap='RdBu_r')
    plt.title('Matrix of Coefficients')
    plt.savefig(directory+'coefficient_matrix'+name+'.png')

    sigma = np.sd(residuals)
    L = (N/2.)*np.log(2*np.pi)-N*np.log(sigma)-(1./sigma**2.)*np.sum(residuals**2.)    
    print(('LIKELIHOOD',L))
    


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

