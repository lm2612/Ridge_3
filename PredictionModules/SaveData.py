import netCDF4
import os
import numpy as np
from GetDir import GetDir
def SaveFile(filename,y,lon,lat,names):
    """ Saves y into netcdf file under filename in datadirectory """
    datadir=GetDir()

    savefile = datadir+filename+'.nc'
    print(savefile)
    # Copy dimension and information for meta data
    dataset = netCDF4.Dataset(savefile, 'w',format='NETCDF4_CLASSIC')

    print(dataset)
    # create dimensions
    lonlat = dataset.createDimension('lonlat',len(lon)*len(lat))
    strlen = dataset.createDimension('strlen', None)

    samples = dataset.createDimension('samples',len(names))
    # create variables
    samples_list = dataset.createVariable('samples_list','S1',('samples','strlen'))
    sample_str = netCDF4.stringtochar(np.array(names))
    samples_list[:] = sample_str

    y_pred = dataset.createVariable('y_pred', np.float64,('samples','lonlat'))
    y_pred[:,:] = y

def ReadFile(filename):
    """ obtains y_pred from netcdf file called filename in datadirectory"""
    datadir=GetDir()

    readfile = datadir+filename+'.nc'
    print(readfile)
    # Copy dimension and information for meta data
    dataset = netCDF4.Dataset(readfile, 'r',format='NETCDF4_CLASSIC')
    y = dataset.variables['y_pred'][:]
    names = netCDF4.chartostring(dataset.variables['samples_list'][:])

    return y,list(names)
