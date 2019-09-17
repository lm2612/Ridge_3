# SpatialTest.py
# Fri 2 Feb 11:15 
#
# lm2612
#

# Import packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as mpatches
from  sklearn.metrics import r2_score

def Scatter(xj,yj,ax = None,title='',ylabel='',xlabel='',xmax=None,ymax=None,colors=None,markers=None,labels=None,line=True):
	if ax == None:
		# Create plot
		fig = plt.figure(figsize=(5,5))
		ax = plt.gca()
	if xmax == None: 
		xmax = 3.
	if ymax == None:
		ymax = 5.
	N = len(xj)
	if colors is None:
		colors = cm.rainbow(np.linspace(0, 1, N))
	if markers is not None:
		for n in range(N):
			ax.scatter(xj[n],yj[n],color=colors[n],marker=markers[n],label=labels[n])	
	else:
		ax.scatter(xj,yj,color=colors,label=labels)
	ax.axis(xmin=-xmax, xmax=xmax, ymin=-ymax, ymax=ymax)
	ax.set_title(title)
	ax.set_ylabel(ylabel)
	ax.set_xlabel(xlabel)

	if line is True:
		A = np.vstack([xj,np.ones(len(xj))]).T	
		(beta,y0),res,rank,s = np.linalg.lstsq(A,yj)
		y_pred = beta*xj+y0
		r2=r2_score(yj, y_pred)
		rmse = np.sqrt(((yj - y_pred) ** 2).mean())	
		line=ax.plot(xj,y_pred,'k-',label='slope=%.3f\nR2=%.3f'%(beta,r2))
		hand,lab = ax.get_legend_handles_labels()
		handles,labels=hand[0:1],lab[0:1]
		ax.legend(handles,labels,loc='lower left',fontsize=8)

	return ax


