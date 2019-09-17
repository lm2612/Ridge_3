import netCDF4

print("Open netcdf file")
# On Monsoon
datadir = '/projects/ukca-imp/laman/AllFiles/'

# On Laura's Mac
#datadir = '/Users/lm2612/Documents/PhD/data/'


savedir = datadir+'AvgData/'
readfile = savedir+'Atmos.nc'

print(readfile)
# Copy dimension and information for meta data
dataset = netCDF4.Dataset(readfile, 'r',format='NETCDF4_CLASSIC')

print(dataset)
# Get sample list
Samples = dataset.variables['samples_list'][:]
Files = netCDF4.chartostring(Samples)

# Get input vars eg. sfc temperature
X_SfcTemp_1 = dataset.variables['SfcTemp_1'][:]
X_AirTemp_1 = dataset.variables['AirTemp_1'][:]
X_GeoHeight_1 = dataset.variables['GeoHeight_1'][:]
X_SLP_1 = dataset.variables['SLP_1'][:]

X_SfcTemp_5 = dataset.variables['SfcTemp_5'][:]
X_AirTemp_5 = dataset.variables['AirTemp_5'][:]
X_GeoHeight_5 = dataset.variables['GeoHeight_5'][:]
X_SLP_5 = dataset.variables['SLP_5'][:]


X_SfcTemp_25 = dataset.variables['SfcTemp_25'][:]
X_AirTemp_25 = dataset.variables['AirTemp_25'][:]
X_GeoHeight_25 = dataset.variables['GeoHeight_25'][:]
X_SLP_25 = dataset.variables['SLP_25'][:]



# Lons and lats

lons = dataset.variables['longitude'][:]
lons1 = dataset.variables['longitude_1'][:]
lats = dataset.variables['latitude'][:]
lats1 = dataset.variables['latitude_1'][:]


nlon = len(lons)
nlat= len(lats)
# Files are saved in code format e.g xikzu , etc. 
# Convert to Full names using dictionary in FileCodesToName.py
print(Files)

from FileCodesToName import *
filecodes = Files
AtmosNames = []
for i in range(len(filecodes)):
    print(i, filenames[filecodes[i]])
    AtmosNames.append(filenames[filecodes[i]])


print(AtmosNames)
