print("Import everything: including opening files, etc. ")
import numpy as np
from GetDir import *
from ReadAvgFiletyr import *

datadir = GetDir()
time = 5

filename = datadir+'All_input_Allfixed_%syrALL_October2019.nc'%time
(X_SfcTemp,X_AirTemp500,X_GeoHeight500,X_SLP,X_RF,y,
 lons,lats,lons1,lats1,Names) = OpenFile(filename)
print((lons,lats))
