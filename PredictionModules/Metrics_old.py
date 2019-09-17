from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from AreaWeighting import Area
import numpy as np
import pandas as pd

def CalcMetrics(y_test,y_pred,areas_flat):
    """ For this y_test, y_pred and weighting areas_flat, returns the following metrics in an array in this order: MODEL MEAN,PREDICTED MEAN, MODEL STD DEV,PREDICTED STD DEV, RMS, MAX MEAN SQ ERROR, MEAN ABS ERROR, MAX ABS ERROR, RMS PATTERN, R2, EXP VAR,NRMS"""
    print((y_test,y_pred,areas_flat))
    mean_y_test = np.average(y_test,weights=areas_flat)
    mean_y_pred = np.average(y_pred,weights=areas_flat)
        
    std_y_test = np.sqrt(np.average((y_test - mean_y_test)**2.,weights=areas_flat))
    std_y_pred = np.sqrt(np.average((y_pred - mean_y_pred)**2.,weights=areas_flat))

    # RMS on overall differences
    rms_sk = np.sqrt( mean_squared_error(y_test,y_pred,areas_flat))
    abs_change = np.average(np.abs(y_test),weights=areas_flat)
    nrms = rms_sk/abs_change

    # Max Mean square
    rms = ((y_test - y_pred)**2)
    max_rms = np.max(rms)

    # Mean absolute error
    mean_abs = mean_absolute_error(y_test,y_pred,areas_flat)

    # max abs error
    abs_err = np.sqrt((y_test-y_pred)**2)
    max_abs = np.max(abs_err)
               
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

    return [mean_y_test, mean_y_pred, std_y_test, std_y_pred, rms_sk, max_rms, mean_abs, max_abs, rms_pattern, r2, exp_var,nrms]



def Metrics(y_pred_all,y_test_all,lons1,lats1, filenames_train, filenames_test,savefolder=None,BestAlpha=None):
    """ Calculates and returns important metrics for comparison of y_pred
    against true values y_test : including RMS (global avg, max abs value, avg in region of NH, avg in region of perturbed emission, avg in region of emission and neighboring regions eg. oceans), correlations between y_pred and y_test """
    areas = Area(lons1,lats1)
    areas_flat = areas.flatten() # Should now be same size as y_pred
    N,p = y_pred_all.shape
    print((N,p))
    print(('trained on :', filenames_train,
    "METRICS: MODEL MEAN, PREDICTED MEAN, MODEL STD DEV, PREDICTED STD DEV, RMS, MAX MEAN SQ ERROR, MEAN ABS ERROR, MAX ABS ERROR, RMS PATTERN, R2, EXP VAR, NORMALISED RMS" ))
    Metrics_titles = ['Model Mean','Predicted Mean','Model Std Dev','Predicted Std Dev', 'RMSE','Max MSE','Mean Abs Err','Max Abs Err','RMSE Pattern','R2','Expl Var','NMRS']

    N_metrics = len(Metrics_titles)
    global_metrics_all = np.zeros((N,N_metrics))
    NHML_metrics_all = np.zeros((N,N_metrics))
    NH_metrics_all = np.zeros((N,N_metrics))
    Regional_metrics_all = np.zeros((N,N_metrics))

    for n in range(N):
        y_test = y_test_all[n,:]
        y_pred = y_pred_all[n,:]
        filename = filenames_test[n] 

        global_metrics = CalcMetrics(y_test,y_pred,areas_flat)
        global_metrics_all[n,:] = global_metrics


        # Check NHML metrics and NH metrics
        NHML_grid = RegionGrids['NHML']
        # Give 0 weighting to regions outside NHML
        NHML_metrics = CalcMetrics(y_test,y_pred,areas_flat*NHML_grid)
        NHML_metrics_all[n,:] = NHML_metrics


        # NH metric
        NH_grid = RegionGrids['NH']
        NH_metrics = CalcMetrics(y_test,y_pred,areas_flat*NH_grid)        
        NH_metrics_all[n,:] = NH_metrics


        # Print regional metrics, if not global
        region = RegionContained(filename)
        print(region)
        if region is not 'Global':
            Regional_grid = RegionGrids[region]
            Regional_metrics = CalcMetrics(y_test,y_pred,areas_flat*Regional_grid)
            Regional_metrics_all[n,:] = Regional_metrics
        else:
            Regional_metrics_all[n,:] = None
    if savefolder is None:
        return Metrics_titles,filenames_train,filenames_test,global_metrics_all,NHML_metrics_all,NH_metrics_all,Regional_metrics_all

    # Otherwise, save files to savefolder
    # Save Metrics to csv file so can be opened in Excel

    N_test = len(filenames_test)
    N_metrics = len(Metrics_titles)
    Metrics_titles_full = []
    global_metrics_full = np.empty(0)
    NHML_metrics_full = np.empty(0)
    NH_metrics_full = np.empty(0)
    Regional_metrics_full = np.empty(0)

    if BestAlpha is not None:
        Metrics_titles_full.append('This run was done with alpha %s'%(BestAlpha['alpha']))
        global_metrics_full=np.append(global_metrics_full, None)
        NHML_metrics_full=np.append(NHML_metrics_full, None)
        NH_metrics_full=np.append(NH_metrics_full, None)
        Regional_metrics_full=np.append(Regional_metrics_full, None)

    for i in range(N_test):
        # Create space between test runs with title of test run
        Metrics_titles_full.append('TEST %s:  %s'%(i+1,filenames_test[i]))
        global_metrics_full=np.append(global_metrics_full, None)
        NHML_metrics_full=np.append(NHML_metrics_full, None)
        NH_metrics_full=np.append(NH_metrics_full, None)
        Regional_metrics_full=np.append(Regional_metrics_full, None)

        # Add metrics
        Metrics_titles_full = Metrics_titles_full+ Metrics_titles
        global_metrics_full = np.append(global_metrics_full,global_metrics_all[i,:])
        NHML_metrics_full = np.append(NHML_metrics_full,NHML_metrics_all[i,:])
        NH_metrics_full = np.append(NH_metrics_full,NH_metrics_all[i,:])
        Regional_metrics_full = np.append(Regional_metrics_full,Regional_metrics_all[i,:])

    print((len(global_metrics_full)))
    print((len(Metrics_titles_full)))

    raw_data = {'METRICS':Metrics_titles_full,
            'Global': global_metrics_full ,
            'NHML': NHML_metrics_full,
            'NH': NH_metrics_full,
            'Regional': Regional_metrics_full}
    df = pd.DataFrame(raw_data,columns = ['METRICS','Global','NHML','NH','Regional'])
    df.to_csv(savefolder+'Metrics.csv')

    return Metrics_titles,filenames_train,filenames_test,global_metrics_all,NHML_metrics_all,NH_metrics_all,Regional_metrics_all


def GlobalMetrics(y_pred,y_test,lons1,lats1, filenames_train, filenames_test,savefolder=None,areas_flat=None):
    Ntest =len(y_pred)
    areas_flat=np.array([1.0])

    Metrics_titles=['Model Mean','Predicted Mean','Model Std Dev','Predicted Std Dev', 'RMSE','Max MSE','Mean Abs Err','Max Abs Err','RMSE Pattern','R2','Expl Var','NMRS']
    N_metrics = len(Metrics_titles)

    global_metrics_all = np.zeros((Ntest,N_metrics))
    for i in range(Ntest):
        global_metrics = CalcMetrics(np.array(y_test[i]),np.array(y_pred[i]),areas_flat)
        global_metrics_all[i] = global_metrics
 
    # save
    Metrics_titles_full = []
    global_metrics_full = np.empty(0)

    for i in range(Ntest):
        # Create space between test runs with title of test run
        Metrics_titles_full.append('TEST %s:  %s'%(i+1,filenames_test[i]))
        global_metrics_full=np.append(global_metrics_full, None)

        # Add metrics
        Metrics_titles_full = Metrics_titles_full+ Metrics_titles
        global_metrics_full = np.append(global_metrics_full,global_metrics_all[i,:])




    raw_data = {'METRICS':Metrics_titles_full,
                'Global': global_metrics_full }

    df = pd.DataFrame(raw_data,columns = ['METRICS','Global'])
    df.to_csv(savefolder+'Metrics.csv')

    return Metrics_titles,filenames_train,filenames_test,global_metrics_all



def RegionalMetrics(y_pred,y_test,Regions,lons1,lats1, filenames_train, filenames_test,savefolder=None,areas_flat=None):
    Ntest,Nregs =(y_pred.shape)
    print((Nregs,Ntest))
    areas_flat = np.array([1.0])

    Metrics_titles=['Model Mean','Predicted Mean','Model Std Dev','Predicted Std Dev', 'RMSE','Max MSE','Mean Abs Err','Max Abs Err','RMSE Pattern','R2','Expl Var','NMRS']
    N_metrics = len(Metrics_titles)
    Metrics_titles_full = []
    for i in range(Ntest):
        # Create space between test runs with title of test run
        Metrics_titles_full.append('TEST %s:  %s'%(i+1,filenames_test[i]))
        # Add metrics
        Metrics_titles_full = Metrics_titles_full+ Metrics_titles

    raw_data = {'METRICS':Metrics_titles_full}
    for j in range(Nregs):
        reg = Regions[j]
        print(reg)
        regional_metrics_all = np.zeros((Ntest,N_metrics))
        global_metrics_full = np.empty(0)
        for i in range(Ntest):
            global_metrics = CalcMetrics(np.array([y_test[i,j]]),np.array([y_pred[i,j]]),areas_flat)
            regional_metrics_all[i] = global_metrics

            global_metrics_full=np.append(global_metrics_full, None)
            global_metrics_full = np.append(global_metrics_full,regional_metrics_all[i,:])

        raw_data[reg] = global_metrics_full

    print(raw_data)

    colnames = ['METRICS']+Regions
    print(colnames)
    df = pd.DataFrame(raw_data,columns = colnames)
    df.to_csv(savefolder+'RegionalMetrics.csv')
