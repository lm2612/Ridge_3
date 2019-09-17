from ImportData import *
from PredictionData import *
from sklearn.preprocessing import scale
X_names = ['SfcTemp','GeoHeight','RF','SfcTempScaled',
      'GeoHeightScaled','RFScaled','SfcTemp,GeoHeight',
      'SfcTemp,RF','GeoHeight,RF','SfcTemp,GeoHeight,RF']
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

X_names = X_names[6:]
Xs = Xs[6:]
for (Xname,X) in zip(X_names,Xs):
    
    d = PredictionData(X,y,Names,lons,lats,lons1,lats1)

    X_types = ['PCA']
    y_types = ['PCA']

    vals = list(range(1,30))
    options = ['Inter']
    for i in vals:
        options.append('Random_%s'%i)
    savedir=('/Users/lm2612/Documents/PhD/plots/RegressionPlots/MetricsRF/')
    for i in range(len(X_types)):
        X_type = X_types[i]
        if (X_type == 'Regional') and ( (Xname!= 'SfcTemp' )or (Xname !='RF')):
            continue
        if ((Xname != 'SfcTemp') or (Xname!= 'RF') or (Xname!='GeoHeight') ) and (X_type != 'PCA') :
            continue
        for j in range(len(y_types)):
            y_type = y_types[j]
            print(i,j,X_type,y_type)
            name_of_file='X=%s_'%Xname
            for option in options:
                d.re_initialise()
           
                d.runRF(option)
                saveas=savedir+name_of_file+option+'_'
                d.metrics(saveas)



