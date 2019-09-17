import sys
sys.path.insert(0, '../UMDataModules/')
sys.path.insert(0, '../Inputs/')
sys.path.insert(0, '../PlotModules/')
sys.path.insert(0, '../PredictionModules/')
print((sys.path))
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

savedir = '/general/user/lm2612/home/WORK/R2plots/'
directory = '/rds/general/user/lm2612/home/WORK/Full/plots/'
filestart = 'X=SfcTemp_Full,y=Full__'
Names = names[:]
regions_all = ['Global','Europe','China','East_Asia','India','Arctic',
              'US','South_America','Austrailia','Africa','NHML','NH']
regions_all = RegionsList

all_predictions = np.zeros((len(Names),192*145))
all_true = np.zeros((len(Names),192*145))


def run_one(directory,name,regions_all,i):
    # open file
    filename = directory+filestart+name+'_data' 
    d = pickle.load(open(filename,'rb') )
    print(d)
    print((d.alpha_params))
    saveas = directory+name+'_R2plots_training'
    all_predictions[i,:]=d.y_pred
    all_true[i,:]=d.y_test
    return(d)   

    

processes = [run_one(directory,name,regions_all,i) for (name,i) in zip(Names,list(range(len(Names))))]
r2_err = r2_score(all_true, all_predictions, multioutput='raw_values')
r2_err = np.reshape(r2_err,(145,192))
print((r2_err))
d=processes[0]
saveas = directory+'allruns_R2plot.png'
plotmap(d.lons,d.lats,r2_err,savefile=saveas,levels=np.arange(0.,1.04,0.01),
            plottitle='R2 error')
N = 26
p = 145*192

r2_adj = 1.-(1.-r2_err)*(N-1.)/(N-p-1.)
#r2_adj = r2_err- (1.-r2_err)*p/(N-p-1.)
saveas  = directory+'allruns_adjR2plot.png'
plotmap(d.lons,d.lats,r2_adj,savefile=saveas,levels=np.arange(0.,1.04,0.01),
            cmap='Reds',plottitle='Adjusted R2 error')
