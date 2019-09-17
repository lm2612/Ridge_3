import numpy as np


def Area1(lons,lats):
    """ Calculates area weighting given longitude and latitudes 
    returns the areas in an array of length nlat-1 x nlon (i.e. on lon1,lat1 grid) """
    # Need radius of earth
    a = 6.371E6
    nlon,nlat = len(lons),len(lats)-1
    
    # For this data, longitude is evenly spaced
    dlon = 2*np.pi/nlon
    # Latitude is not evenly spaced

    areas = np.zeros((nlat,nlon))
    for j in range(nlat):
        dlatj = (np.pi/180.)*(lats[j+1]-lats[j])*np.cos(np.pi*(lats[j+1]+lats[j])/360.)
        areas[j,:] = (a**2)*dlon*dlatj

    return areas




def Area(lons1,lats1):
    """ Calculates area weighting given longitude and latitudes 
    returns the areas in an array of length nlat+1 x nlon (i.e. on lon,lat grid) """
    # Need radius of earth
    a = 6.371E6
    nlon,nlat = len(lons1),len(lats1)+1

    # For this data, longitude is evenly spaced
    dlon = 2*np.pi/nlon
    # Latitude is not evenly spaced

    areas = np.zeros((nlat,nlon))
    lats = np.insert(lats1,0,-90.)
    lats = np.append(lats,[90.])
    for j in range(0,nlat):
        dlatj = (np.pi/180.)*(lats[j+1]-lats[j])*np.cos(np.pi*(lats[j+1]+lats[j])/360.)
        areas[j,:] = (a**2)*dlon*dlatj


    return areas
