from ImportData import *
from PredictionData import *
from sklearn.preprocessing import scale
from sklearn.preprocessing import MinMaxScaler
from remove_ind import remove_ind
from SaveData import *
from remove_ind import *
#Names,(X_SfcTemp,y)=remove_ind(Names,'No Dust Arabia',(X_SfcTemp,y))

# What is the predictor X?
X = X_SfcTemp
X_name = 'SfcTemp'

# Any dimension reduction (eg PCA) or full grid?
X_type = 'Full'
y_type = 'Full'


# alpha for regularisation, no of CV
alpha_list = np.logspace(-1,4,200)
no_of_cv = 5

# where to save?
savedir = '/home/lm2612/plots/full_test/'
save_filename = 'X=SfcTemp_Full,y=Full_'

# regions of interest for metrics?
regions_all = ['Global','Europe','Sahel','US','China','East_Asia','India','NHML','Tropics','Africa','South_America','SHML','Arctic','Austrailia','NH','Tropics','SHML']


d = PredictionData(X,y,Names,lons,lats,lons1,lats1)
d.setup(X_type,y_type)

d.save_X()

# Loop over all predictions
for name in Names[20:]:
    print(name)
    d.re_initialise()
    d.run(X_type,y_type,'Ridge',name,cvfolds=no_of_cv,alpha_list = alpha_list)
    
    saveas = savedir+save_filename+name+'_'

    d.metrics_regional(saveas,regions_all)
    d.plot_results(savedir+'plots/')

