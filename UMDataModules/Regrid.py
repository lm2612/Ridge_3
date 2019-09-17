import numpy as np
from scipy.interpolate import interp2d
def Regridder(X,lons,lats,newlons,newlats):
    f= interp2d(lons,lats,X) 
    Xregrid = f(newlons,newlats)
    return(Xregrid)


def ReduceRes(vars_to_reduce,lons,lats,factor_lat=None,factor_lon=None,nlat=None,nlon=None):
    """ provide either new nlat nlon or factor to divide by for lon and lat
    we call mid resolution 144/2, 192/2
    low res 144/4, 192/4 """
    if nlat is None:
        if nlon is None:
            if factor_lon is None:
                factor_lon = factor_lat
            # Regrid onto lower res grid
            nlon = int(len(lons)/factor_lon)
            nlat = int(len(lats)/factor_lat)
    p = nlon*nlat
    # keep min and max of current lons and lats, linearly space
    newlons = np.linspace(np.min(lons),np.max(lons),nlon)
    newlats = np.linspace(np.min(lats),np.max(lats),nlat)

    nlat1 = len(newlats)-1
    nlon1 = len(newlons)
    lats1 = np.zeros(nlat1)
    lons1 = newlons
    for i in range(nlat1):
        lats1[i] = (newlats[i]+newlats[i+1])/2.
    print(lats1)

    # Need to grid it for each sample
    New_vars = []
    for X_orig in vars_to_reduce:
        print((X_orig.shape))
        N = X_orig.shape[0]
        Xnew = np.zeros((N,p))
        ynew = np.zeros((N,p))
        for i in range(N):
            X = np.reshape(X_orig[i,:],(len(lats),len(lons)))
            X_regridded = Regridder(X,lons,lats,newlons,newlats)
            X_flat = X_regridded.flatten()
            Xnew[i,:] = X_flat
        New_vars.append(Xnew)

    return(New_vars,newlons,newlats)
