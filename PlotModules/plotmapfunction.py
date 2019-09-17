#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 08:12:02 2017

@author: lm2612
"""
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap,shiftgrid

def plotmap(lons,lats,variable,savefile=None, cmap="RdBu_r", levels=None,
            variable_label='',plottitle='',plotaxis=None,colorbar=1.0):
    """ Plots a map and displays output or saves to file with path 
    and filename savefile (string). Inputs are lons, lats and the variable
    in format they are outputted from ReadFile (ie from netcdf file). 
    also cmap is colour- eg for tempchange choose RdBu_r"""
    if plotaxis is None:
        plt.clf()
    
    map = Basemap()
    # draw coastlines, country boundaries, fill continents.
    map.drawcoastlines(linewidth=0.25)
    map.drawcountries(linewidth=0.25)
    
    # draw the edge of the map projection region (the projection limb)
    map.drawmapboundary(fill_color='lightseagreen')
    # draw lat/lon grid lines every 30 degrees.
    map.drawmeridians(np.arange(0,360,30))
    map.drawparallels(np.arange(-90,90,30))

    variable,lons = shiftgrid(180.,variable,lons,start=False)

    # Check variable is on same grid as lons and lats: may need to correct
    # lat levels if they are on stagged grid 
    #if variable.shape[0] != len(lats):
    #    centred_lats = np.zeros(len(lats)-1)
    #    centred_lats[:] = lats[1:]-(lats[1:]-lats[0:-1])/2.
    #    lats = centred_lats

    # Create lon lat grid for plotting
    longrid,latgrid = np.meshgrid(lons,lats)
    
    # Plot map
    cmap = map.contourf(longrid,latgrid,variable,cmap=cmap,lonlat=True,
                        levels=levels,extend='both')
    if colorbar == 1.0:
        cbar = map.colorbar()
        cbar.set_label(variable_label)
    
    plt.xlabel('Longitude')
    plt.xticks(np.arange(-180.,185.,90.))
    plt.yticks(np.arange(-90.,91.,30.))
    plt.ylabel('Latitude')
    plt.title(plottitle)
    plt.tight_layout()

    if type(savefile) is str:
        plt.savefig(savefile)
        print('Saved plot as '+savefile)
    
    
    return map, cmap 
