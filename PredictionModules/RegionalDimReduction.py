import numpy as np
from ReadRegions import *
import scipy
def split_into_regions(X,areas_flat,lons,lats,lons1,lats1,Regions=['Europe','US','China','East_Asia','India','NHML','NH'],return_area=False):
    """ Takes full X defined at each longitude and latitude and
    returns a reduced X for inputs that are averaged over N key
    regions provided (or default is
    [US,Europe,China,EastAsia,India,NHML,NH]- these regions must be
    defined in ReadRegions file )
    NOTE- written for X but works also for y 
        """
    Nreg = len(Regions)
    N,p = X.shape
    print(p)
    print(areas_flat.shape)
        
    # Create new array with Nreg dimensions instead of p
    Xnew = np.zeros((N,Nreg))
    areas = np.zeros((N,Nreg))
    for i in range(Nreg):
        region = Regions[i]
        print('Region %s'%region)        
        grid = RegionGrids[region]
        print(grid.shape)
        if grid.shape != areas_flat.shape:
            # hard coding- apologies
            fullgrid_nlon = 192
            fullgrid_nlat = 145
            fullgrid_lons = np.arange(0.,360,1.875)
            fullgrid_lats = np.linspace(-90.,90.0,fullgrid_nlat)
            fullgrid = grid.reshape((fullgrid_nlat,fullgrid_nlon))
            f = scipy.interpolate.interp2d(fullgrid_lats,fullgrid_lons,fullgrid.T)
            if (len(lons1)*len(lats1) == len(areas_flat)):
                newgrid = f(lats1,lons1).T
            elif (len(lons)*len(lats) == len(areas_flat)):
                newgrid = f(lats,lons).T
            grid = newgrid.flatten()
        # Calc over this avg with correct weighting 
        print(X.shape, (areas_flat*grid).shape)
        Xavg = np.average(X,axis=1,weights=areas_flat*grid)    
        Xnew[:,i] = Xavg
        areas[:,i] = np.sum(areas_flat*grid)/np.sum(areas_flat)
    if return_area:
        return Xnew,areas
    else:
        return Xnew
