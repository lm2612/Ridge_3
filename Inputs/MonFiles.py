import numpy as np
import netCDF4
import glob
import sys
import os
from CalcSeasonalAvg import *

time = 5
def ReadVariables(open_file):
    print("file, ",open_file)
    # Get all
    names_of_vars = ['air_temperature','geopotential_height','surface_temperature','air_pressure_at_sea_level']
    ps = [5,5,None,None]
    airtemp,geoheight,sfctemp,slp = GetVariable(open_file,names_of_vars,ps)
    print(airtemp.shape)
    # Do avgs :
    # Get air temperature
    dataseason = MonthlyToSeasonal(airtemp)
    AirTemp500 = np.mean(dataseason[:,0:time],axis=1)

    # Get geopotential height 
    dataseason = MonthlyToSeasonal(geoheight)
    GeoHeight500 = np.mean(dataseason[:,0:time],axis=1)

    # Get temperature at surface
    dataseason = MonthlyToSeasonal(sfctemp)
    SfcTemp = np.mean(dataseason[:,0:time],axis=1)
    OutputTemp = np.mean(dataseason[:,50:],axis=1)

    # Get SLP
    dataseason = MonthlyToSeasonal(slp)
    SLP = np.mean(dataseason[:,0:time],axis=1)    
    return AirTemp500,GeoHeight500,SfcTemp,OutputTemp,SLP

def ReadVariablesMatt(open_file):
    print("file, ",open_file)
    # Get air temperature
    dataseason = GetVariable(open_file,'air_temperature',p=5,dT=4)
    AirTemp500 = np.mean(dataseason[:,0:time],axis=1)
    print(AirTemp500.shape)
    # Get geopotential height 
    dataseason = GetVariable(open_file,'geopotential_height',p=5,dT=4)
    GeoHeight500 = np.mean(dataseason[:,0:time],axis=1)


    # Get temperature at surface
    dataseason = GetVariable(open_file,'surface_temperature',dT=4)
    SfcTemp = np.mean(dataseason[:,0:time],axis=1)
    OutputTemp = np.mean(dataseason[:,50:],axis=1)


    # Get SLP
    dataseason = GetVariable(open_file,'air_pressure_at_sea_level',dT=4)
    SLP = np.mean(dataseason[:,0:time],axis=1)


    return AirTemp500,GeoHeight500,SfcTemp,OutputTemp,SLP


# Read in data
datadir = '/projects/ukca-imp/laman/AllFiles/'


# Matt's Data
Matt_Coupled = (glob.glob(datadir+'Matt_Coupled_monthly/*.pp'))
Matt_Atmos = (glob.glob(datadir+'Matt_Atmos_New/*.pp'))

Matt_Control = [datadir+'Matt_Coupled_monthly/xizko.pp',datadir+'Matt_Coupled_monthly/xizka.pp',datadir+'Matt_Coupled_monthly/xizkp.pp',datadir+'Matt_Coupled_monthly/xkhqb.pp',datadir+'Matt_Coupled_monthly/xkhqc.pp',datadir+'Matt_Coupled_monthly/xkhqd.pp']
Matt_Control.remove(datadir+'Matt_Coupled_monthly/xizka.pp')
# Remove ctrl run from list of main runs (deal with this separately and remove from perturbed runs)

for ctrl in Matt_Control:
	Matt_Coupled.remove(ctrl)

# Also remove small BC forcings s.ppe these are noisy
# No BC Europe
Matt_Coupled.remove(datadir+'Matt_Coupled_monthly/xizkx.pp')
# No BC East Asia
Matt_Coupled.remove(datadir+'Matt_Coupled_monthly/xizkl.pp')
# No BC US
Matt_Coupled.remove(datadir+'Matt_Coupled_monthly/xizky.pp')

# PDRMIP
PDRMIP_Coupled = (glob.glob(datadir+'PDRMIP_Coupled_monthly/*.pp'))
PDRMIP_Atmos = (glob.glob(datadir+'PDRMIP_Atmos_New/*.pp'))

PDRMIP_Control = datadir+'PDRMIP_Coupled_monthly/xkcxa.pp'
PDRMIP_Coupled.remove(PDRMIP_Control)


# ECLIPSE
ECLIPSE_Coupled = (glob.glob(datadir+'ECLIPSE_Coupled_monthly/*.pp'))
ECLIPSE_Atmos = (glob.glob(datadir+'ECLIPSE_Atmos_New/*.pp'))

ECLIPSE_Control_fixedCH4 = datadir+'ECLIPSE_Coupled_monthly/xixak.pp'
ECLIPSE_Control_intCH4 = datadir+'ECLIPSE_Coupled_monthly/xixap.pp'
ECLIPSE_Coupled.remove(ECLIPSE_Control_fixedCH4)
ECLIPSE_Coupled.remove(ECLIPSE_Control_intCH4)

nMatt = len(Matt_Coupled)
nPDRMIP = len(PDRMIP_Coupled) 
nECLIPSE = len(ECLIPSE_Coupled) 

nTOTAL = nMatt + nPDRMIP + nECLIPSE
nALL = len(Matt_Coupled+PDRMIP_Coupled+ECLIPSE_Coupled)


nlat_y = 145
nlon_y = 192
ny_features = nlon_y*nlat_y

nlat_x = 144
nlon_x = 192
nx_features = (nlon_x*nlat_x)

n_samples = nTOTAL
print("Number of samples = ",n_samples)


# Get X and y from datasets
ntime = 4 # Seasonal
X_SfcTemp = np.zeros((ntime,n_samples,ny_features))
X_AirTemp500 = np.zeros((ntime,n_samples,nx_features))
X_GeoHeight500 = np.zeros((ntime,n_samples,nx_features))
X_SLP = np.zeros((ntime,n_samples,ny_features))
y = np.zeros((ntime,n_samples,ny_features))
index = 0

# First read in Matt's data
print(" Reading in Matt's data .... ")

# Control runs:
nMattCtrl = len(Matt_Control)


for i in range(nMattCtrl):
    open_file = Matt_Control[i]
    AirTemp500,GeoHeight500,SfcTemp,OutputTemp,SLP=ReadVariablesMatt(open_file)
    if i==0:
	AirTemp500Ctrl,GeoHeight500Ctrl,SfcTempCtrl,OutputTempCtrl,SLPCtrl= AirTemp500/float(nMattCtrl),GeoHeight500/float(nMattCtrl),SfcTemp/float(nMattCtrl),OutputTemp/float(nMattCtrl),SLP/float(nMattCtrl)
    else:
	AirTemp500Ctrl += AirTemp500/float(nMattCtrl)
	GeoHeight500Ctrl += GeoHeight500/float(nMattCtrl)
	SfcTempCtrl += SfcTemp/float(nMattCtrl)
	OutputTempCtrl +=OutputTemp/float(nMattCtrl)
	SLPCtrl += SLP/float(nMattCtrl)


# Full Data
for i in range(nMatt):
    open_file = Matt_Coupled[i]
    AirTemp500,GeoHeight500,SfcTemp,OutputTemp,SLP=ReadVariablesMatt(open_file)
    
    # Remove control run and flatten in lons and lats
    for s in range(4):
        X_AirTemp500[s,index,:] =(AirTemp500[s]-AirTemp500Ctrl[s]).flatten()
        X_GeoHeight500[s,index,:] = (GeoHeight500[s]-GeoHeight500Ctrl[s]).flatten()
        X_SfcTemp[s,index,:] = (SfcTemp[s] - SfcTempCtrl[s]).flatten()
        X_SLP[s,index,:] = (SLP[s] - SLPCtrl[s]).flatten()
        y[s,index,:] = (OutputTemp[s]-OutputTempCtrl[s]).flatten()
    index += 1

print("Matt's data: DONE ")

# Second read in PDRMIP data

print(" Reading in PDRMIP data ... ")
# Only 1 ctrl run
open_file = PDRMIP_Control

AirTemp500Ctrl,GeoHeight500Ctrl,SfcTempCtrl,OutputTempCtrl,SLPCtrl=ReadVariables(open_file)
print(AirTemp500Ctrl)
# Full Data

for i in range(nPDRMIP):
    open_file = PDRMIP_Coupled[i]
    AirTemp500,GeoHeight500,SfcTemp,OutputTemp,SLP=ReadVariables(open_file)

    # Remove control run
    for s in range(4):
        X_AirTemp500[s,index,:] = (AirTemp500[s]-AirTemp500Ctrl[s]).flatten()
        X_GeoHeight500[s,index,:] = (GeoHeight500[s]-GeoHeight500Ctrl[s]).flatten()
        X_SfcTemp[s,index,:] = (SfcTemp[s] - SfcTempCtrl[s]).flatten()
        X_SLP[s,index,:] =(SLP[s] - SLPCtrl[s]).flatten()
	y[s,index,:] = (OutputTemp[s]-OutputTempCtrl[s]).flatten()
    index += 1


print("PDRMIP data: DONE ")
print(y.shape)
print(X_AirTemp500.shape)

# Finally ECLIPSE

print(" Reading in ECLIPSE data ... ")
# 2 ctrl runs which go with different runs
open_file = ECLIPSE_Control_fixedCH4

AirTemp500Ctrlf,GeoHeight500Ctrlf,SfcTempCtrlf,OutputTempCtrlf,SLPCtrlf=ReadVariables(open_file)

open_file = ECLIPSE_Control_intCH4

AirTemp500Ctrli,GeoHeight500Ctrli,SfcTempCtrli,OutputTempCtrli,SLPCtrli=ReadVariables(open_file)

# Full Data
for i in range(nECLIPSE):
    open_file = ECLIPSE_Coupled[i]
    AirTemp500,GeoHeight500,SfcTemp,OutputTemp,SLP=ReadVariables(open_file)

    # Remove control run
    if open_file in [datadir+'ECLIPSE_Coupled_monthly/xixam.pp',datadir+'ECLIPSE_Coupled_monthly/xixan.pp',datadir+'ECLIPSE_Coupled_monthly/xixao.pp',datadir+'ECLIPSE_Coupled_monthly/xixav.pp']:
        for s in range(4):
            X_AirTemp500[s,index,:] =(AirTemp500[s]-AirTemp500Ctrlf[s]).flatten()
            X_GeoHeight500[s,index,:] = (GeoHeight500[s]-GeoHeight500Ctrlf[s]).flatten()
            X_SfcTemp[s,index,:] = (SfcTemp[s] - SfcTempCtrlf[s]).flatten()
            X_SLP[s,index,:] = (SLP[s] - SLPCtrlf[s]).flatten()
	    y[s,index,:] = (OutputTemp[s]-OutputTempCtrlf[s]).flatten()
    	index += 1

    else:
	for s in range(4):
            X_AirTemp500[s,index,:] = (AirTemp500[s]-AirTemp500Ctrli[s]).flatten()
            X_GeoHeight500[s,index,:] = (GeoHeight500[s]-GeoHeight500Ctrli[s]).flatten()
            X_SfcTemp[s,index,:] = (SfcTemp[s] - SfcTempCtrli[s]).flatten()
            X_SLP[s,index,:] = (SLP[s] - SLPCtrli[s]).flatten()
            y[s,index,:] = (OutputTemp[s]-OutputTempCtrli[s]).flatten()
        index += 1

print("ECLIPSE data: DONE ")


print("Completed reading in data (InputsOutputs.py) ")

print("Save data to netcdf file")

AllFiles = Matt_Coupled+PDRMIP_Coupled+ECLIPSE_Coupled
FileNameOnly = Matt_Coupled+PDRMIP_Coupled+ECLIPSE_Coupled
for fi in range(len(AllFiles)):
	filename = AllFiles[fi]
	base=os.path.basename(filename)
	FileNameOnly[fi] = (os.path.splitext(base)[0])
print(AllFiles)

savedir = datadir+'AvgData/'

saveas = savedir+'SeasonalDataMAM-DJF_%syr.nc'%time

dimfile = datadir+'Matt_Coupled_New/xizko.nc'
# Copy dimension and information for meta data
file_in = netCDF4.Dataset(dimfile,'r',format='NETCDF4_CLASSIC')
dims= file_in.dimensions
print(type(dims))
print(dims)






dataset = netCDF4.Dataset(saveas, 'w',format='NETCDF4_CLASSIC')


for dim in dims:
        dimension = dims[dim]
        print(dimension)
        size= len(dimension)
	dim_new = dataset.createDimension(dim,size)



for l in (['longitude','latitude','longitude_1','latitude_1']):
        lon = file_in.variables[l]
        lon_new = dataset.createVariable(l,np.float64,lon.dimensions)
        lon_new[:] = lon[:]
		


lonlat = dataset.createDimension('lonlat',ny_features)
lonlat1 = dataset.createDimension('lonlat1',nx_features)
strlen = dataset.createDimension('strlen', 5)

samples = dataset.createDimension('samples',len(AllFiles))
seasons = dataset.createDimension('seasons',4)

samples_list = dataset.createVariable('samples_list','S1',('samples','strlen'))
sample_str = netCDF4.stringtochar(np.array(FileNameOnly))
samples_list[:] = sample_str

SfcTemp = dataset.createVariable('SfcTemp', np.float64,('seasons','samples','lonlat'))
SfcTemp[:] = X_SfcTemp

AirTemp = dataset.createVariable('AirTemp',np.float64,('seasons','samples','lonlat1'))
AirTemp[:] = X_AirTemp500

GeoHeight = dataset.createVariable('GeoHeight',np.float64,('seasons','samples','lonlat1'))
GeoHeight[:] = X_GeoHeight500

SLP = dataset.createVariable('SLP',np.float64,('seasons','samples','lonlat'))
SLP[:] = X_SLP


SfcTempResponse = dataset.createVariable('SfcTempResponse',np.float64,('seasons','samples','lonlat'))
SfcTempResponse[:] = y






print(samples_list[:])
print(netCDF4.chartostring(samples_list[:]))



print(dataset)
