import sys
sys.path.insert(0, '/home/lm2612/Ridge/RunScripts/')
sys.path.insert(0, '/home/lm2612/Ridge/Inputs/')
sys.path.insert(0, '/home/lm2612/Ridge/PlotModules/')
sys.path.insert(0, '/home/lm2612/Ridge/PredictionModules/')

from RegionLatitudes import * 
from DefineRegions import *
import netCDF4
import os 
from GetDir import GetDir

#RegionsList = ['NHML','China','East_Asia','Europe','India','US','Africa','South_America','Tropics','SHML','Arctic','Sahel','Austrailia','Asia',
#'Arabia','Global','NH','NHML_ext','China_ext','East_Asia_ext','Europe_ext','India_ext','US_ext','Arabia_ext','Africa_ext','South_America_ext']

nlon = 192
nlat = 145
lons = np.arange(0.,360.,360./nlon)
lats = np.arange(-90.,90.,180./nlat)

datadir = GetDir()
save_data = datadir+'Region.nc'


levels = [0., 1.0]

nregions = len(RegionsList)
AllGrids = np.zeros((nregions,nlat*nlon))

for i in range(nregions):
    region = RegionsList[i]
    grid = DefineRegion(region,lons,lats)
    flatgrid = grid.flatten()
    AllGrids[i,:] = flatgrid

# Save
dataset = netCDF4.Dataset(save_data, 'w',format='NETCDF4_CLASSIC')

lonlat = dataset.createDimension('lonlat',nlon*nlat)
regions = dataset.createDimension('regions',nregions)
str_len = dataset.createDimension('str_len')

regions_list = dataset.createVariable('regions_list','S1',('regions','str_len'))

regions_str = netCDF4.stringtochar(np.array(RegionsList))
regions_list[:] = regions_str


Grids = dataset.createVariable('Grids',np.float64,('regions','lonlat'))
Grids[:,:] = AllGrids
