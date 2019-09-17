datadir = '/projects/ukca-imp/laman/AllFiles/PDRMIP_Coupled_monthly/'
matt_dir = '/projects/ukca-imp/laman/AllFiles/Matt_Coupled_monthly/'
import numpy as np
import glob
import iris

pdrmip_files = (glob.glob(datadir+'/*.pp'))
Matt_files = (glob.glob(datadir+'/*.pp'))
cubes = iris.load(pdrmip_files[0])
print(cubes)
def GetVariable(f,names_of_vars,ps,dT=12): 
	""" f is the name of the file to read, name_of_var is a string with name
	of var, can be monthly file or seasonal file, indicated by dT=12 or dT=4 """
	cubes = iris.load(f,names_of_vars)
	Nvar = len(names_of_vars)
	list_of_vars = []
	for v in range(Nvar):
		print(names_of_vars[v])
		p = ps[v]
		cube = cubes[v]
		data = cube.data
		shape = data.shape
		print(shape)
		ntime = shape[0]
		print(ntime)
		nyear = int(np.floor(np.float(ntime)/np.float(dT)))
		nyear = ntime/dT
		if len(shape) == 3:
			ntime,nlat,nlon = shape
			newshape = (dT,nyear,nlat,nlon)
		elif len(shape) == 4:
			ntime,nP,nlat,nlon = shape
			newshape = (dT,nyear,nP,nlat,nlon)
			if type(p) is int:
				data = data[:,p,:,:]
				newshape = (dT,nyear,nlat,nlon)
		else:
			print('error in shape of %s'%name_of_var)
			list_of_vars.append(None)
			continue
		all_mons = np.zeros(newshape)
		for i in range(dT):        	
			data_mon = data[i:ntime:dT]
			print(data_mon.shape)
			if data_mon.shape[0] == nyear:
				all_mons[i] = data_mon
			elif data_mon.shape[0] == nyear-1:
				all_mons[i,0:-1] = data_mon
		list_of_vars.append(all_mons)
		
	return list_of_vars
	        
def MonthlyToSeasonal(all_mons):
	""" Convert monthly avg to seasonal avgs """
	shape = all_mons.shape
	print(shape)
	spatial_dims = shape[1:]
	nseasons = (4,)
	newshape = nseasons+spatial_dims
	print(newshape)
	all_seasons = np.zeros((newshape))
	nt = shape[1]
	month = 0   # start from dec
	for i in range(4):
		print(month,month+3)
		season = all_mons[month:month+3] 
		all_seasons[i] = np.mean(season,axis=0)
		month = month+3
	return all_seasons



