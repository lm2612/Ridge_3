from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score, mean_absolute_error

from sklearn.preprocessing import StandardScaler

from AreaWeighting import Area
from DefineRegions import *
from ReadRegions import *
import numpy as np
import pandas as pd
from RegionalDimReduction import split_into_regions

def CalcMetrics(y_test,y_pred,areas_flat):
    """ For this y_test, y_pred and weighting areas_flat, returns the following metrics in an array in this order: MODEL MEAN,PREDICTED MEAN, MODEL STD DEV,PREDICTED STD DEV, RMS, MAX MEAN SQ ERROR, MEAN ABS ERROR, MAX ABS ERROR, RMS PATTERN, R2, EXP VAR,NRMSE"""
    print((y_test.shape,y_pred.shape,areas_flat.shape))
    mean_y_test = np.average(y_test,weights=areas_flat)
    mean_y_pred = np.average(y_pred,weights=areas_flat)
        
    std_y_test = np.sqrt(np.average((y_test - mean_y_test)**2.,weights=areas_flat))
    std_y_pred = np.sqrt(np.average((y_pred - mean_y_pred)**2.,weights=areas_flat))

    # RMS on overall differences
    mean_sq = mean_squared_error(y_test,y_pred,areas_flat)
    rms_sk = np.sqrt(mean_sq)
    
    # Normalise
    abs_change = np.average(np.abs(y_test),weights=areas_flat)
    pred_abs_change = np.average(np.abs(y_pred),weights=areas_flat)
    nrms = rms_sk/abs_change

    # Max Mean square
    ms = ((y_test - y_pred)**2)
    max_sq = np.max(ms)
    min_sq = np.min(ms)

    # median sq deviation (MAD)
    med_sq = np.median(ms)
    # upper and lower quartiles - gives us distribution of errors
    lq_sq = np.quantile(ms, 0.25)
    uq_sq = np.quantile(ms,0.75)
    sq_errors = {'mean_sq':mean_sq,
                  'median_sq':med_sq,
                  'min_sq':min_sq,
                  'max_sq':max_sq,
                  'lq_sq':lq_sq,
                  'uq_sq':uq_sq}

    # Mean absolute error
    mean_abs = mean_absolute_error(y_test,y_pred,areas_flat)

    # max abs error
    abs_err = np.abs((y_test-y_pred))
    max_abs = np.max(abs_err)
    min_abs = np.min(abs_err)
    
    # median abs deviation (MAD)
    med_abs = np.median(abs_err)
    # upper and lower quartiles - gives us distribution of errors
    lq_abs = np.quantile(abs_err, 0.25)
    uq_abs = np.quantile(abs_err,0.75)
    
    abs_errors = {'mean_abs':mean_abs,
                  'median_abs':med_abs,
                  'min_abs':min_abs,
                  'max_abs':max_abs,
                  'lq_abs':lq_abs,
                  'uq_abs':uq_abs}

    # mean percentage error (note inf when y_test=0)
    per_error = (y_test - y_pred)/y_test
    mean_per = np.average(per_error,weights=areas_flat)
    med_per = np.nanquantile(per_error,0.5)



    # RMS on PATTERN (normalise y_pred and y_test first)
    if std_y_test >0.:
        y_test_scaled = (y_test-mean_y_test)/std_y_test
        y_pred_scaled = (y_pred-mean_y_pred)/std_y_pred
        rms_pattern = np.sqrt( mean_squared_error(y_test_scaled,y_pred_scaled,areas_flat))
    else:
        rms_pattern=rms_sk.copy()
    # R2 error (best is 1.0)
    r2 = r2_score(y_test, y_pred, areas_flat)

    # explained_variance score
    exp_var = explained_variance_score(y_test,y_pred,areas_flat)

    metrics_dict = {'Model Mean':mean_y_test,
                    'Predicted Mean':mean_y_pred,
                    'Model Std Dev':std_y_test,
                    'Predicted Std Dev':std_y_pred,
                    'Model Abs Mean':abs_change,
                    'Predicted Abs Mean':pred_abs_change,
                    'RMSE':rms_sk,
                    'R2':r2,
                    'Expl Var':exp_var,
                    'RMSE Pattern':rms_pattern,
                    'mean_percentage_error':mean_per
                   }
    metrics_dict.update(abs_errors)
    metrics_dict.update(sq_errors)

    return metrics_dict 

def RegionalMetrics(y_pred,y_test,Regions,lons,lats,lons1,lats1, filenames_train, filenames_test,savefolder,areas_flat):
    Ntest,p = y_pred.shape
    print((y_pred.shape))
    # check Ntest == 1
    full_metrics_dict = {}
    Nreg = len(Regions)
    # Do global metrics on full grid
    metrics_dict = CalcMetrics(y_test[0,:],y_pred[0,:],areas_flat)
    # Initialise full metric dictionary and add the full global metrics
    keys = list(metrics_dict.keys())
    full_metrics_dict = {"Regions":["Full Grid"]+Regions+["All Regions"]}
    for key in keys:
        full_metrics_dict[key] = np.zeros((Nreg+2))
        full_metrics_dict[key][0] = metrics_dict[key]
    # Now do regional metrics by taking average over regions
    if (y_pred.shape[1]!=len(Regions)):
        y_pred_reg = split_into_regions(y_pred,areas_flat,
                    lons,lats,lons1,lats1,Regions)
        y_test_reg = split_into_regions(y_test,areas_flat,
                    lons,lats,lons1,lats1,Regions)
    else:
        y_pred_reg = y_pred
        y_test_reg = y_test

    for (i,reg) in zip(list(range(Nreg)),Regions):
        print((i,y_pred_reg[0,i]))
        metrics_dict = CalcMetrics(np.array([y_test_reg[0,i]]),np.array([y_pred_reg[0,i]]),np.array([1.0]))
        for key in list(metrics_dict.keys()):
            full_metrics_dict[key][i+1] = metrics_dict[key]

    metrics_dict = CalcMetrics(y_test_reg[0,:],y_pred_reg[0,:],np.ones(Nreg))
    for key in keys:
        full_metrics_dict[key][Nreg+1] = metrics_dict[key]

    colnames = ["Regions"]+ keys
    print(colnames)
    print(full_metrics_dict)
    df = pd.DataFrame(data=full_metrics_dict,columns = colnames)
    print(df)
    df.to_csv(savefolder+'RegionalMetrics.csv')
    return full_metrics_dict
