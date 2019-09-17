import netCDF4
import os
from GetDir import GetDir
print("Open netcdf file")

def OpenFile(time,filename='All_input'):
        datadir=GetDir()
        print(datadir)
        savedir = datadir+'AvgData/'
        readfile = savedir+filename+'_%syr.nc'%time

        print(readfile)
        # Copy dimension and information for meta data
        dataset = netCDF4.Dataset(readfile, 'r',format='NETCDF4_CLASSIC')

        print(dataset)
        # Get sample list
        Samples = dataset.variables['samples_list'][:]
        Files = netCDF4.chartostring(Samples)

        # Get input vars eg. sfc temperature
        X_SfcTemp = dataset.variables['SfcTemp'][:]
        X_AirTemp500 = dataset.variables['AirTemp'][:]
        X_GeoHeight500 = dataset.variables['GeoHeight'][:]
        X_SLP = dataset.variables['SLP'][:]
	try:
		X_RF = dataset.variables['RF'][:]
	except:
		X_RF = None

        # Output var
        y = dataset.variables['SfcTempResponse'][:]

        # Lons and lats
        nlon = len(dataset.variables['longitude'][:])
        nlat = len(dataset.variables['latitude'][:])

        lons = dataset.variables['longitude'][:]
        lons1 = dataset.variables['longitude_1'][:]
        lats = dataset.variables['latitude'][:]
        lats1 = dataset.variables['latitude_1'][:]


        # Files are saved in code format e.g xikzu , etc. 
        # Convert to Full names using dictionary in FileCodesToName.py
        from FileCodesToName import *
        filecodes = Files
        Names = []
        for i in range(len(filecodes)):
            print(i, filenames[filecodes[i]])
            Names.append(filenames[filecodes[i]])


        print(Names)
        
        return (X_SfcTemp,X_AirTemp500,X_GeoHeight500,X_SLP,X_RF,y,
                nlon,nlat,lons,lons1,lats,lats1,Files,Names)

