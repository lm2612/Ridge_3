from ImportData import *
from PredictionData import *
from sklearn.preprocessing import scale
from remove_ind import remove_ind
# SELECT THIS INFO 
print(Names)
# REMOVE INDICES FOR OUTLIERS
print(X_SfcTemp.shape)
(Names,[X_SfcTemp,X_GeoHeight500,X_RF,y]) = remove_ind(Names,'No Dust Arabia',[X_SfcTemp,X_GeoHeight500,X_RF,y] )
(Names,[X_SfcTemp,X_GeoHeight500,X_RF,y]) = remove_ind(Names,'5X SO4',[X_SfcTemp,X_GeoHeight500,X_RF,y] )

print(Names)
print(X_SfcTemp.shape)

# Choose X and the name which it will be saved under
X1=scale(X_SfcTemp)
X2=scale(X_GeoHeight500)
X3=scale(X_RF)
X1X2=np.concatenate((X1,X2),axis=1)
X1X3=np.concatenate((X1,X3),axis=1)
X2X3=np.concatenate((X2,X3),axis=1)
Xall = np.concatenate((X1,X2,X3),axis=1)

Xs =[X_SfcTemp,X_GeoHeight500,X_RF,X1,
     X2,X3, (X1,X2),
     (X1,X3), (X2,X3), (X1,X2,X3)]
X_names = ['SfcTemp','GeoHeight','RF','SfcTempScaled',
      'GeoHeightScaled','RFScaled','SfcTemp,GeoHeight',
      'SfcTemp,RF','GeoHeight,RF','SfcTemp,GeoHeight,RF']

# Choose parameters to test regularisation overalpha_list=np.logspace(2,7,30)
alpha_list=np.logspace(-1,6,100)
alpha_list = np.concatenate((np.logspace(-16,-1,10),alpha_list))
# Loop over different types of dim reduction
X_types = ['Global mean','Regional','Regional','PCA','Full']
y_types = ['Global mean','Regional','Regional','PCA','Full']
regions_many = ['Europe','US','China','East_Asia','India','NHML','Tropics','Africa','South_America','SHML','Arctic','Austrailia']
regions_few = ['Europe','US','East_Asia','India','Arctic','Sahel']
regions = [None,regions_many,regions_few,None,None]
region_labels=['',str(len(regions_many)),str(len(regions_few)),'','']

X_types=X_types[:3]
y_types=y_types[0:3]
regions = regions[0:3]
region_labels=region_labels[0:3]

# no of cv folds
no_of_cv=5


# where should output be saved?
savedir=('/Users/lm2612/Documents/PhD/plots/RegressionPlots/MetricsCV%sLOO_removedoutliers/'%no_of_cv)


# --------------------------------
# RUN LOOP OVER EVERYTHING

# cross val
options = Names

# Loop over everything
for (Xname,X) in zip(X_names,Xs):
    for i in range(len(X_types)):
        X_type = X_types[i]
        for j in range(len(y_types)):
            y_type = y_types[j]
            print(i,j,X_type,y_type)
            name_of_file = 'X=%s_%s%s,y=%s%s_'%(Xname,X_type,region_labels[i],y_type,region_labels[j])
            # set up variables
            if type(X) is tuple:
                print ('multi var')
                if (X_type == 'Global mean'):
                    d.mean_X()
                    for xi in range(1,len(X)):
                        di = PredictionData(X[xi],y,Names,lons,lats,lons1,lats1)
                        di.mean_X()
                        d.combine_X(di.X,di.area_X)
                    print(d.X)
                elif (X_type == 'Regional'):
                    if ( xi.shape[1]!= 27840 for xi in X):
                        print('Cannot calc regional avgs for %s with dim not eq to 27840'%(Xname))
                        continue
                    d.regional_X(regions[i])
                    for xi in range(1,len(X)):
                        di=PredictionData(X[xi],y,Names,lons,lats,lons1,lats1)
                        di.regional_X(regions[i])
                        d.combine_X(di.X,di.area_X)
                X_type = 'Full'
            else: 
                d = PredictionData(X,y,Names,lons,lats,lons1,lats1)
                d.setup(X_type,y_type,regions[i],regions[j])
                print(d.X)
                print(d.X_type)
            d.save_X()
            for option in options:
                # Re-initialise so the data is not split into training/test sets from previous iteration
                print(option)
                d.re_initialise()
                d.run(X_type,y_type,'Ridge',option,regions[i],regions[j],cvfolds=no_of_cv,alpha_list = alpha_list)
                saveas=savedir+name_of_file+option+'_'
                if y_types[j] == 'Global mean':
                    d.metrics_global(saveas)
                elif y_types[j] == 'Regional':
                    d.metrics_regional(saveas)
		else:
                    d.metrics(saveas)
                    d.metrics_regional(saveas,['Global']+regions_few)


