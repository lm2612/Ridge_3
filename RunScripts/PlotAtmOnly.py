from ImportData import *
from plotmapfunction import *
# Import Atmos only data
(X_SfcTemp_Atm,X_AirTemp500_Atm,X_GeoHeight500_Atm,X_SLP_Atm,X_RF_Atm,y_Atm,
                lons,lats,lons1,lats1,Names_Atm) = OpenFile(datadir+'Atmos_15yr.nc',
['SfcTemp_1','AirTemp_1','GeoHeight_1','SLP_1',
                      'RF_1','SfcTempResponse_1'])

# Put in same order
N_atm = len(Names_Atm)
N_cpl,p = y.shape
print("N_cpl %s, N_atm %s, "%(N_cpl,N_atm))
new_y = np.zeros((N_atm,p))

for atm_ind in range(N_atm):
        name = Names_Atm[atm_ind]
        print(atm_ind,name)

        cpl_ind = Names.index(name)
        print(cpl_ind)
        new_y[atm_ind,:] = y[cpl_ind,:]
y = new_y.copy()

Names = Names_Atm
savedir = '/work/lm2612/fsst_eqmplots/'
nlat = len(lats)
nlon = len(lons)
for i in range(N_atm):
    saveas=savedir+Names[i]+'.png'

    ax1 = plt.subplot2grid((2, 1), (0, 0))
    ax2 = plt.subplot2grid((2, 1), (1, 0))
    temp_in = X_SfcTemp_Atm[i,:].reshape((nlat,nlon))
    temp_out = y[i,:].reshape((nlat,nlon))
    maxtemp = np.ceil(0.4*np.max([np.abs(temp_out),np.abs(temp_in)]))
    levels = np.arange(-maxtemp,maxtemp+0.01,maxtemp/10.)
    plt.sca(ax1)
    plotmap(lons,lats,temp_in,cmap='RdBu_r',variable_label='K',
     levels=levels, plottitle='Fixed SST eqm temp change',plotaxis=ax1)
    plt.sca(ax2)
    plotmap(lons,lats,temp_out,cmap='RdBu_r',levels=levels, variable_label='K',
      plottitle='Coupled eqm temp change',plotaxis=ax2)

    plt.savefig(saveas)
    print("Saved ",saveas)
    plt.close()

