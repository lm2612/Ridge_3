import numpy as np
from mpl_toolkits.basemap import maskoceans,shiftgrid
def LandSeaMask(lons,lats,datain):
    """ Returns land sea mask on grid of size nlat * nlon """
    nlat,nlon = len(lats),len(lons)
    data_gridded = np.reshape(datain,(nlat,nlon))
    # shift onto -180 to 180 domain suitable for basemap maskoceans
    datain,lons = shiftgrid(180.,data_gridded,lons,start=False)
    # need full grid for lons and lats
    lonsin = np.zeros((nlat,nlon))
    latsin = np.zeros((nlat,nlon))
    for i in range(nlat):
        lonsin[i,:] = lons
    for i in range(nlon):
        latsin[:,i] = lats
    dataout = maskoceans(lonsin,latsin,datain)
    # shift back and flatten
    dataout,lons = shiftgrid(0,dataout,lons,True)
    data_flat = dataout.flatten()
    return(data_flat)
