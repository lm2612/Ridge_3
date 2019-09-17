from PredictionData import *

filenames = glob.glob('/rdsgpfs/general/user/lm2612/home/WORK/RemoveNoiseNew/plots/*data')
list_of_alpha = []
for file in filenames:
    new_data=pickle.load(open(file,'rb'))
    list_of_alpha.append(new_data.alpha_params['alpha'])
    
filenames = [file.split('__')[-1].split('_data')[0] for file in filenames]

alphas = {}

for i in range(len(list_of_alpha)):
    alphas[filenames[i]] = list_of_alpha[i]
    
pickle.dump(alphas,open('/rdsgpfs/general/user/lm2612/home/WORK/RemoveNoiseNew/plots/alphas','wb') )