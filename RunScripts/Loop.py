from ImportData import *
from PredictionData import *
from sklearn.preprocessing import scale
# SELECT THIS INFO 

# Choose X and the name which it will be saved under
X1=scale(X_SfcTemp)
X2=scale(X_GeoHeight500)
X3=scale(X_RF)
X1X2=np.concatenate((X1,X2),axis=1)
X1X3=np.concatenate((X1,X3),axis=1)
X2X3=np.concatenate((X2,X3),axis=1)
Xall = np.concatenate((X1,X2,X3),axis=1)

Xs =[X_SfcTemp,X_GeoHeight500,X_RF,X1,
     X2,X3, X1X2,
     X1X3, X2X3, Xall]
X_names = ['SfcTemp','GeoHeight','RF','SfcTempScaled',
      'GeoHeightScaled','RFScaled','SfcTemp,GeoHeight',
      'SfcTemp,RF','GeoHeight,RF','SfcTemp,GeoHeight,RF']

# Choose parameters to test regularisation over
alpha_list=np.logspace(2,7,100)

# No of times to run cross validation
no_of_cross_vals = 30

# Loop over different types of dim reduction
X_types = ['Global mean','Regional','Regional','PCA']
y_types = ['Global mean','Regional','Regional','PCA']
regions_many = ['Europe','US','China','East_Asia','India','NHML','Tropics','Africa','South_America','SHML','Arctic','Austrailia']
regions_few = ['Europe','US','East_Asia','India','Arctic','Sahel']
regions = [None,regions_many,regions_few,None]
region_labels=['',str(len(regions_many)),str(len(regions_few)),'']


# where should output be saved?
savedir=('/Users/lm2612/Documents/PhD/plots/RegressionPlots/MetricsCV10/')



# --------------------------------
# RUN LOOP OVER EVERYTHING

# cross val
vals = list(range(1,no_of_cross_vals))
options = ['Inter']
for i in vals:
    options.append('Random_%s'%i)


for (Xname,X) in zip(X_names,Xs):
    d = PredictionData(X,y,Names,lons,lats,lons1,lats1)
    for i in range(len(X_types)):
        X_type = X_types[i]
        if (X_type == 'Regional') and ( (Xname!= 'SfcTemp' )or (Xname !='RF')):
            continue
        if ((Xname != 'SfcTemp') or (Xname!= 'RF') or (Xname!='GeoHeight') ) and (X_type != 'PCA') :
            continue
        for j in range(len(y_types)):
            y_type = y_types[j]
            print(i,j,X_type,y_type)
            name_of_file = 'X=%s_%s%s,y=%s%s_'%(Xname,X_type,region_labels[i],y_type,region_labels[j])
            for option in options:
                d.re_initialise()
           
                d.run(X_type,y_type,'Ridge',option,regions[i],regions[j],cvfolds=10,alpha_list = alpha_list)
                saveas=savedir+name_of_file+option+'_'
                if y_types[j] == 'Global mean':
                    d.metrics_global(saveas)
                elif y_types[j] == 'Regional':
                    d.metrics_regional(saveas)
                elif y_types[j] == 'PCA':
                    d.metrics(saveas)
                    d.metrics_regional(saveas,['Global']+regions_few)



