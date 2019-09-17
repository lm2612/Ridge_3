import numpy as np
#import cf
import netCDF4
import glob
import sys

def ReadVariables(open_file):
    dataset = netCDF4.Dataset(open_file,'r',format='NETCDF4_CLASSIC')
    # Get air temperature
    temp = dataset.variables['temp_1']
    data= temp[0:10,:,:,:]
    AirTemp = np.mean(data,axis=0)
    AirTemp500 = AirTemp[5,:,:].flatten()
    AirTempAll = AirTemp.flatten()

    # Get geopotential height 
    geo = dataset.variables['ht']
    data = geo[0:10,:,:,:]
    GeoHeight = np.mean(data,axis=0)
    GeoHeight500 = GeoHeight[5,:,:].flatten()
    GeoHeightAll = GeoHeight.flatten()


    # Get temperature at surface
    tempsfc = dataset.variables['temp']
    data = tempsfc[0:10,:,:,:]
    SfcTemp = np.mean(data,axis=0)
    SfcTemp = SfcTemp.flatten()


    # Mean over last 50/150 yrs for output
    outputdata = tempsfc[50:,0,:,:]
    OutputTemp = np.mean(outputdata,axis = 0)
    OutputTemp = OutputTemp.flatten()

    # Get SLP
    slp = dataset.variables['p']
    data = slp[0:10,:,:,:]
    SLP = np.mean(data,axis=0)
    SLP = SLP.flatten()


    # Get Radiative Forcing
    SWin = dataset.variables['field200'][0:1,0,:,:]
    SWout = dataset.variables['field201'][0:1,0,:,:]
    LWout = dataset.variables['olr'][0:1,0,:,:]
    data = SWin - SWout - LWout
    RF = np.mean(data,axis=0)
    RF = RF.flatten()


    
    return AirTemp500,AirTempAll,GeoHeight500,GeoHeightAll,SfcTemp,OutputTemp,SLP,RF

# Read in data
datadir = '/projects/ukca-imp/laman/AllFiles/'
# Matt's Data
Matt_Coupled = (glob.glob(datadir+'Matt_Coupled_New/*.nc'))
Matt_Atmos = (glob.glob(datadir+'Matt_Atmos_New/*.nc'))

Matt_Control = [datadir+'Matt_Coupled_New/xizko.nc',datadir+'Matt_Coupled_New/xizka.nc',datadir+'Matt_Coupled_New/xizkp.nc',datadir+'Matt_Coupled_New/xkhqb.nc',datadir+'Matt_Coupled_New/xkhqc.nc',datadir+'Matt_Coupled_New/xkhqd.nc']

# Remove ctrl run from list of main runs (deal with this separately and remove from perturbed runs)

for ctrl in Matt_Control:
	Matt_Coupled.remove(ctrl)

# Also remove small BC forcings since these are noisy
# No BC Europe
Matt_Coupled.remove(datadir+'Matt_Coupled_New/xizkx.nc')
# No BC East Asia
Matt_Coupled.remove(datadir+'Matt_Coupled_New/xizkl.nc')
# No BC US
Matt_Coupled.remove(datadir+'Matt_Coupled_New/xizky.nc')


# PDRMIP
PDRMIP_Coupled = (glob.glob(datadir+'PDRMIP_Coupled_New/*.nc'))
PDRMIP_Atmos = (glob.glob(datadir+'PDRMIP_Atmos_New/*.nc'))

PDRMIP_Control = datadir+'PDRMIP_Coupled_New/xkcxa.nc'
PDRMIP_Coupled.remove(PDRMIP_Control)


# ECLIPSE
ECLIPSE_Coupled = (glob.glob(datadir+'ECLIPSE_Coupled_New/*.nc'))
ECLIPSE_Atmos = (glob.glob(datadir+'ECLIPSE_Atmos_New/*.nc'))

ECLIPSE_Control_fixedCH4 = datadir+'ECLIPSE_Coupled_New/xixak.nc'
ECLIPSE_Control_intCH4 = datadir+'ECLIPSE_Coupled_New/xixap.nc'
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
X_SfcTemp = np.zeros((n_samples,ny_features))
X_AirTemp500 = np.zeros((n_samples,nx_features))
X_AirTempAll = np.zeros((n_samples,nx_features*17))
X_GeoHeight500 = np.zeros((n_samples,nx_features))
X_GeoHeightAll = np.zeros((n_samples,nx_features*17))
X_SLP = np.zeros((n_samples,ny_features))
X_RF = np.zeros((n_samples,ny_features))
y = np.zeros((n_samples,ny_features))
index = 0

# First read in Matt's data
print(" Reading in Matt's data .... ")

# Control runs:
nMattCtrl = len(Matt_Control)
for i in range(nMattCtrl):
    open_file = Matt_Control[i]
    AirTemp500,AirTempAll,GeoHeight500,GeoHeightAll,SfcTemp,OutputTemp,SLP,RF=ReadVariables(open_file)
    if i==0:
	AirTemp500Ctrl,AirTempAllCtrl,GeoHeight500Ctrl,GeoHeightAllCtrl,SfcTempCtrl,OutputTempCtrl,SLPCtrl,RFCtrl = AirTemp500/float(nMattCtrl),AirTempAll/float(nMattCtrl),GeoHeight500/float(nMattCtrl),GeoHeightAll/float(nMattCtrl),SfcTemp/float(nMattCtrl),OutputTemp/float(nMattCtrl),SLP/float(nMattCtrl),RF/float(nMattCtrl)
    else:
	AirTemp500Ctrl += AirTemp500/float(nMattCtrl)
	AirTempAllCtrl += AirTempAll/float(nMattCtrl)
	GeoHeight500Ctrl += GeoHeight500/float(nMattCtrl)
	GeoHeightAllCtrl += GeoHeightAll/float(nMattCtrl)
	SfcTempCtrl += SfcTemp/float(nMattCtrl)
	OutputTempCtrl +=OutputTemp/float(nMattCtrl)
	SLPCtrl += SLP/float(nMattCtrl)
	RFCtrl += RF/float(nMattCtrl)


# Full Data
for i in range(nMatt):
    open_file = Matt_Coupled[i]
    AirTemp500,AirTempAll,GeoHeight500,GeoHeightAll,SfcTemp,OutputTemp,SLP,RF=ReadVariables(open_file)
    
    # Remove control run
    X_AirTempAll[index,:] = AirTempAll-AirTempAllCtrl
    X_AirTemp500[index,:] = AirTemp500-AirTemp500Ctrl
    X_GeoHeightAll[index,:] = GeoHeightAll-GeoHeightAllCtrl
    X_GeoHeight500[index,:] = GeoHeight500-GeoHeight500Ctrl
    X_SfcTemp[index,:] = SfcTemp - SfcTempCtrl
    X_SLP[index,:] = SLP - SLPCtrl
    X_RF[index,:] = RF - RFCtrl

    y[index,:] = OutputTemp-OutputTempCtrl 
    
    index += 1

print("Matt's data: DONE ")

# Second read in PDRMIP data

print(" Reading in PDRMIP data ... ")
# Only 1 ctrl run
open_file = PDRMIP_Control

AirTemp500Ctrl,AirTempAllCtrl,GeoHeight500Ctrl,GeoHeightAllCtrl,SfcTempCtrl,OutputTempCtrl,SLPCtrl,RFCtrl=ReadVariables(open_file)

# Full Data

for i in range(nPDRMIP):
    open_file = PDRMIP_Coupled[i]
    AirTemp500,AirTempAll,GeoHeight500,GeoHeightAll,SfcTemp,OutputTemp,SLP,RF=ReadVariables(open_file)

    # Remove control run
    X_AirTempAll[index,:] = AirTempAll-AirTempAllCtrl
    X_AirTemp500[index,:] = AirTemp500-AirTemp500Ctrl
    X_GeoHeightAll[index,:] = GeoHeightAll-GeoHeightAllCtrl
    X_GeoHeight500[index,:] = GeoHeight500-GeoHeight500Ctrl
    X_SfcTemp[index,:] = SfcTemp - SfcTempCtrl
    X_SLP[index,:] = SLP - SLPCtrl
    X_RF[index,:] = RF - RFCtrl


    y[index,:] = OutputTemp-OutputTempCtrl
    index += 1


print("PDRMIP data: DONE ")

# Finally ECLIPSE

print(" Reading in ECLIPSE data ... ")
# 2 ctrl runs which go with different runs
open_file = ECLIPSE_Control_fixedCH4

AirTemp500Ctrlf,AirTempAllCtrlf,GeoHeight500Ctrlf,GeoHeightAllCtrlf,SfcTempCtrlf,OutputTempCtrlf,SLPCtrlf,RFCtrlf=ReadVariables(open_file)

open_file = ECLIPSE_Control_intCH4

AirTemp500Ctrli,AirTempAllCtrli,GeoHeight500Ctrli,GeoHeightAllCtrli,SfcTempCtrli,OutputTempCtrli,SLPCtrli,RFCtrli=ReadVariables(open_file)

# Full Data
for i in range(nECLIPSE):
    open_file = ECLIPSE_Coupled[i]
    AirTemp500,AirTempAll,GeoHeight500,GeoHeightAll,SfcTemp,OutputTemp,SLP,RF=ReadVariables(open_file)

    # Remove control run
    if open_file in [datadir+'ECLIPSE_Coupled_New/xixam.nc',datadir+'ECLIPSE_Coupled_New/xixan.nc',datadir+'ECLIPSE_Coupled_New/xixao.nc',datadir+'ECLIPSE_Coupled_New/xixav.nc']:
    	X_AirTempAll[index,:] = AirTempAll-AirTempAllCtrlf
     	X_AirTemp500[index,:] = AirTemp500-AirTemp500Ctrlf
     	X_GeoHeightAll[index,:] = GeoHeightAll-GeoHeightAllCtrlf
    	X_GeoHeight500[index,:] = GeoHeight500-GeoHeight500Ctrlf
    	X_SfcTemp[index,:] = SfcTemp - SfcTempCtrlf
	X_SLP[index,:] = SLP - SLPCtrlf
        X_RF[index,:] = RF - RFCtrlf

    	y[index,:] = OutputTemp-OutputTempCtrlf
    	index += 1

    else:
	X_AirTempAll[index,:] = AirTempAll-AirTempAllCtrli
        X_AirTemp500[index,:] = AirTemp500-AirTemp500Ctrli
        X_GeoHeightAll[index,:] = GeoHeightAll-GeoHeightAllCtrli
        X_GeoHeight500[index,:] = GeoHeight500-GeoHeight500Ctrli
        X_SfcTemp[index,:] = SfcTemp - SfcTempCtrli
	X_SLP[index,:] = SLP - SLPCtrli
   	X_RF[index,:] = RF - RFCtrli

        y[index,:] = OutputTemp-OutputTempCtrli
        index += 1

print("ECLIPSE data: DONE ")


print("Completed reading in data (InputsOutputs.py) ")



