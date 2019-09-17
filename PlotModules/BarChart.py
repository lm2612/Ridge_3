# Creates bar chart for regional
import matplotlib.pyplot as plt

def BarChart(y_pred,y_true,xlabels,title,savefolder):
	""" Creates bar chart for y_pred and y_true """
	plt.clf()
	xlocs = list(range(len(xlabels)))
	plt.bar(xlocs,y_pred,align='center')
	plt.plot(xlocs,y_true,'kx')
	plt.xticks(xlocs,[xlabel.replace('_',' ') for xlabel in xlabels],rotation=45)
	plt.title(title)
	plt.ylabel('Predicted Temp Response in Region (K)')
	saveas = savefolder+'BarChart_'+title+'.png'
	plt.tight_layout()
	plt.savefig(saveas)
	print('Bar Chart saved as ',saveas)

