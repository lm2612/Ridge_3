from ImportData import *
from PredictionData import *
import pickle
from sklearn.decomposition import PCA
import glob
npcs = [1,2,3,5,10,15,20,25]
filedir =['/work/lm2612/PCA/pca_output_%s/'%(n for n in npcs)]
for dr,n in zip(filedir,npcs):
    filenames = glob.glob(dr+'*output')
    for filename in filenames:
        name = filenames.split('/')[-1].split('_output')[0]
        
        d = pickle.load(open(filename,'rb'))
        y_pred = d.y_pred
        y_test = d.y_test

        pca_y = d.pca_y
        pc_pred = pca_y(y_pred)
        pc_test = pca_y(y_test)
        print((pc_pred,pc_test))
        exit()
