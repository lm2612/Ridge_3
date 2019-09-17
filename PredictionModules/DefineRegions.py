# Import dictionary containing region latitudes
from RegionLatitudes import *
import numpy as np
def ConditionFunction(lon,lat,lonmin,lonmax,latmin,latmax):
    """ Simple condition statement returning 1 if falls in region or 0 otherwise"""
    if lon>= lonmin and lon<=lonmax and lat>=latmin and lat<=latmax:
        return 1.0
    else:
        return 0.0

def ConditionFunction_Overlap(lon,lat,lonmin,lonmax,latmin,latmax):
    """ If regoin overlaps the longitude=0 axis (e.g. Europe) treat differently
    with a new condition statement """
    if (lon>=lonmin or lon<=lonmax) and lat>=latmin and lat<=latmax:
        return 1.0
    else:
        return 0.0

def DefineRegion(region,lons,lats):
    """ Defines a grid containing 0. outside the region and 1.0 inside region
    based on maximum and minimum lons and lats provided in RegionLonsLats
    dictionary in RegionLatitudes """
    nlon , nlat = len(lons), len(lats)
    # Get min and max lons and lats from dict in RegionLatitudes
    lonmin,lonmax,latmin,latmax=RegionLonsLats[region]
    # Initialise grid
    grid = np.zeros((nlat,nlon))

    # Must treat regions that overlap the lon = 0 axis differently 
    # with different condition function
    if lonmin > lonmax:
        Condition = ConditionFunction_Overlap
    else:
        Condition = ConditionFunction


    for i in range(nlon):
        lon = lons[i]
        for j in range(nlat):
            lat = lats[j]
            grid[j,i] = Condition(lon,lat,lonmin,lonmax,latmin,latmax)
    
    return grid

def RegionContained(experimentname):
    """ Finds region contained within experimentname e.g. No SO2 China returns China """
    ListOfRegs = ['China','NHML','Arabia','East_Asia','Asia','Europe','India','US']
    for reg in ListOfRegs:
        if reg in experimentname:
            return reg
        else:
            continue 
    
    return 'Global'




