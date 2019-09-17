"""
Created on Thu Jan 25 12:06:59 2018

@author: lm2612
"""
# Import
import matplotlib.cm as cm
from plotmapfunction import *
import datetime
from sklearn.metrics import mean_squared_error

def PredictionPlot(y_test,y_pred_test,lons,lats, filenames_train, filenames_test, savefolder,rmses):
    """ Plots predicted and true model output in graph for easy comparison """
    now = datetime.datetime.now()
    imshape = (100, 9)
    print(now)
    timestamp = datetime.datetime.strftime(now,"%d-%m_%H%M")

    plt.rcParams['font.size'] = 8
    for t in range(y_pred_test.shape[0]):
        runname = filenames_test[t]
        print(t,runname)
        rmse = rmses[t]

        nlon,nlat = len(lons),len(lats)

        y_reshaped = y_test[t,:].reshape((nlat,nlon))
        y_pred_reshaped = y_pred_test[t,:].reshape((nlat,nlon))
   
        absmax =  np.max(np.abs(y_reshaped))
        yplot_pred = y_pred_reshaped
        maxlvl = np.ceil(absmax*0.8)

        levels = np.arange(-maxlvl,maxlvl+0.01,0.2)
        plt.clf()
        fig = plt.figure(figsize=(11,5))


        ax2 = plt.subplot2grid((2, 2), (0, 0))
        ax3 = plt.subplot2grid((2, 2), (0, 1))
        ax4 = plt.subplot2grid((2, 2), (1, 0))
        ax5 = plt.subplot2grid((2, 2), (1, 1))


        plt.sca(ax2)
        plotmap(lons,lats,y_pred_reshaped,cmap='RdBu_r',
            levels=levels, variable_label='Temperature Response (K)',
            plottitle='Predicted',
            plotaxis=ax2)

        plt.sca(ax3)
        absmax =  np.max(np.abs(y_reshaped))
        yplot = y_reshaped 
        plotmap(lons,lats,y_reshaped,cmap='RdBu_r',levels=levels,
                variable_label='Temperature Response (K)',
                plottitle='True Model',
                plotaxis=ax3)
   
        plt.sca(ax4)
        plotmap(lons,lats,yplot_pred-yplot,cmap='RdBu_r',
                levels=np.arange(-2.,2.1,0.1),variable_label='Temperature Difference (K)',
                plottitle='Absolute Difference: (Predicted - True)',
                plotaxis=ax4)

        plt.sca(ax5)
        divide = (yplot_pred - yplot)/np.abs(yplot)
        plotmap(lons,lats,divide,cmap = 'RdBu_r', 
                plottitle='Fractional Difference: (Prediction - True)/|True| ',variable_label='Fractional Difference',
                levels=np.arange(-3.0,3.1,0.2),plotaxis=ax5)


        fig.suptitle(runname)
        savefileas = savefolder+'%s_%s.png'%(runname.replace(' ','_'),timestamp)
        plt.savefig(savefileas,bbox_inches='tight')
        print("Saved as ",savefileas)
        plt.close()
