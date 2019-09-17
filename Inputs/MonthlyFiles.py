import numpy as np
import netCDF4
import glob
import sys
import os
from CalcSeasonalAvg import *

time = 5
def ReadVariables(open_file,dT=12):
    """ Reads in the 5 regions of interest and averages over them (monthly)"""
    print("file, ",open_file)
    # Get all
    names_of_vars = ['air_temperature','geopotential_height','surface_temperature','air_pressure_at_sea_level']
    ps = [5,5,None,None]
    airtemp,geoheight,sfctemp,slp = GetVariable(open_file,names_of_vars,ps,dT)
    print("shape before avging:", airtemp.shape)
    return airtemp,geoheight,sfctemp,slp

def TakeAvgs(airtemp,geoheight,sfctemp,slp,time):
    # Do avgs :
    # Air temp
    AirTemp500 = np.mean(airtemp[:,0:time],axis=1)
    # geopotential height 
    GeoHeight500 = np.mean(geoheight[:,0:time],axis=1)
    # Get temperature at surface
    SfcTemp = np.mean(sfctemp[:,0:time],axis=1)
    OutputTemp = np.mean(sfctemp[:,50:],axis=1)
    # Get SLP
    SLP = np.mean(slp[:,0:time],axis=1)    
    return AirTemp500,GeoHeight500,SfcTemp,OutputTemp,SLP

def RemoveCtrl(perturbed_vars,ctrl_vars):
    """ calcs difference between perturb and ctrl for all variables in this list: requires arrays the same size """
    anomalies = []
    perturbed_vars=list(perturbed_vars)
    ctrl_vars = list(ctrl_vars)
    Nvar = len(perturbed_vars)
    for n in range(Nvar):
	pert = perturbed_vars[n]
	ctrl = ctrl_vars[n]
        try:
	    anom=pert-ctrl
        except:
	    print("pert, ctrl diff sizes")
	    npert = pert.shape[0]
	    nctrl = ctrl.shape[0]
	    N = min(npert,nctrl)   
	    anom=npert-nctrl
        anomalies.append(anom)
    return anomalies


# Read in data
datadir = '/projects/ukca-imp/laman/AllFiles/'
PDRMIP_Coupled = (glob.glob(datadir+'PDRMIP_Coupled_monthly/*.pp'))

PDRMIP_Control = datadir+'PDRMIP_Coupled_monthly/xkcxa.pp'
PDRMIP_Coupled.remove(PDRMIP_Control)


# ECLIPSE
ECLIPSE_Coupled = (glob.glob(datadir+'ECLIPSE_Coupled_monthly/*.pp'))

ECLIPSE_Control_fixedCH4 = datadir+'ECLIPSE_Coupled_monthly/xixak.pp'
ECLIPSE_Control_intCH4 = datadir+'ECLIPSE_Coupled_monthly/xixap.pp'
ECLIPSE_Coupled.remove(ECLIPSE_Control_fixedCH4)
ECLIPSE_Coupled.remove(ECLIPSE_Control_intCH4)

nPDRMIP = len(PDRMIP_Coupled) 
nECLIPSE = len(ECLIPSE_Coupled) 

nTOTAL = nPDRMIP + nECLIPSE
nALL = len(PDRMIP_Coupled+ECLIPSE_Coupled)


nlat_y = 145
nlon_y = 192
ny_features = nlon_y*nlat_y

nlat_x = 144
nlon_x = 192
nx_features = (nlon_x*nlat_x)

n_samples = nTOTAL
print("Number of samples = ",n_samples)


# Get X and y from datasets
ntime = 12 # Monthly
X_SfcTemp = np.zeros((ntime,n_samples,ny_features))
X_AirTemp500 = np.zeros((ntime,n_samples,nx_features))
X_GeoHeight500 = np.zeros((ntime,n_samples,nx_features))
X_SLP = np.zeros((ntime,n_samples,ny_features))
y = np.zeros((ntime,n_samples,ny_features))
index = 0


# First read in PDRMIP data

print(" Reading in PDRMIP data ... ")
# Only 1 ctrl run
open_file = PDRMIP_Control

allctrls = ReadVariables(open_file)
# Full Data

for i in range(nPDRMIP):
    open_file = PDRMIP_Coupled[i]
    allperts=ReadVariables(open_file)
    allanoms=RemoveCtrl(allperts,allctrls)
    (airtemp,geoheight,sfctemp,slp)=tuple(allanoms)
    AirTemp500,GeoHeight500,SfcTemp,OutputTemp,SLP=TakeAvgs(airtemp,geoheight,sfctemp,slp,time)
    print("after avging: ", AirTemp500.shape)
    for s in range(ntime):
        X_AirTemp500[s,index,:] = (AirTemp500[s]).flatten()
        X_GeoHeight500[s,index,:] = (GeoHeight500[s]).flatten()
        X_SfcTemp[s,index,:] = (SfcTemp[s]).flatten()
        X_SLP[s,index,:] =(SLP[s]).flatten()
	y[s,index,:] = (OutputTemp[s]).flatten()
    index += 1


print("PDRMIP data: DONE ")
print(X_SfcTemp)
print(y.shape)
print(X_AirTemp500.shape)

# Finally ECLIPSE

print(" Reading in ECLIPSE data ... ")
# 2 ctrl runs which go with different runs
open_file = ECLIPSE_Control_fixedCH4
allctrlsf = ReadVariables(open_file)

open_file = ECLIPSE_Control_intCH4
allctrlsi = ReadVariables(open_file)

# Full Data
for i in range(nECLIPSE):
    open_file = ECLIPSE_Coupled[i]
    allperts=ReadVariables(open_file)
    if open_file in [datadir+'ECLIPSE_Coupled_monthly/xixam.pp',datadir+'ECLIPSE_Coupled_monthly/xixan.pp',datadir+'ECLIPSE_Coupled_monthly/xixao.pp',datadir+'ECLIPSE_Coupled_monthly/xixav.pp']:
        allanoms=RemoveCtrl(allperts,allctrlsf)
    else:
	allanoms=RemoveCtrl(allperts,allctrlsi)
    (airtemp,geoheight,sfctemp,slp)=tuple(allanoms)
    AirTemp500,GeoHeight500,SfcTemp,OutputTemp,SLP=TakeAvgs(airtemp,geoheight,sfctemp,slp,time)
    print("after avging: ", AirTemp500.shape)

    for s in range(ntime):
        X_AirTemp500[s,index,:] = (AirTemp500[s]).flatten()
        X_GeoHeight500[s,index,:] = (GeoHeight500[s]).flatten()
        X_SfcTemp[s,index,:] = (SfcTemp[s]).flatten()
        X_SLP[s,index,:] =(SLP[s]).flatten()
        y[s,index,:] = (OutputTemp[s]).flatten()
    index += 1


print("ECLIPSE data: DONE ")

print("Completed reading in data (InputsOutputs.py) ")

print("Save data to netcdf file")

AllFiles = PDRMIP_Coupled+ECLIPSE_Coupled
FileNameOnly = PDRMIP_Coupled+ECLIPSE_Coupled
for fi in range(len(AllFiles)):
	filename = AllFiles[fi]
	base=os.path.basename(filename)
	FileNameOnly[fi] = (os.path.splitext(base)[0])
print(AllFiles)

savedir = datadir+'AvgData/'

saveas = savedir+'SeasonalData_Dec-Jan_%syr.nc'%time

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
seasons = dataset.createDimension('seasons',12)

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
