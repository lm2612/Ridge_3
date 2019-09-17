import netCDF4
import os
from GetDir import GetDir
datadir = GetDir()
readfile = datadir+'Region.nc'

# Copy dimension and information for meta data
dataset = netCDF4.Dataset(readfile, 'r',format='NETCDF4_CLASSIC')

# Get sample list
Reg = dataset.variables['regions_list'][:]
Regions = netCDF4.chartostring(Reg)

# Get input vars eg. sfc temperature
Grids = dataset.variables['Grids'][:]

RegionGrids = {}

for i in range(len(Regions)):
	RegionGrids[Regions[i]] = Grids[i,:]

print(RegionGrids)

