import numpy as np
import netCDF4
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA


import sys
sys.path.insert(0,  '../UMDataModules/')
sys.path.insert(0,  '../Inputs/')
sys.path.insert(0,  '../PlotModules/')
sys.path.insert(0,  '../UMDataModules/')



from AreaWeighting import * 
from RegionalDimReduction import split_into_regions
from RegressionFunction import Regression
from Metrics import *
from PlotPredictionVsTrue_NoScaling import PredictionPlot


class PredictionData():
    def __init__(self, X, y, names, lons, lats, lons1, lats1):
        self.X_raw = X
        self.y_raw = y
        self.X = self.X_raw.copy()
        self.y = self.y_raw.copy()
        area = Area(lons1, lats1).flatten()
        self.area_y = area.copy()
        p = X.shape[-1]
        if p == len(lons)*len(lats):
            self.area_X = area.copy()
            self.lons_X = lons
            self.lats_X = lats
        elif p == len(lons1)*len(lats1):
            area = Area1(lons, lats)
            self.area_X = area.flatten()
            self.lons_X = lons1
            self.lats_X = lats1
        elif p < 20:
            print('X is a regional or global avg')
            self.area_X = np.ones(p)
        else:
            print('X is combination of variables')
            self.area_X = None

        self.lons = lons
        self.lats = lats
        self.lons1 = lons1
        self.lats1 = lats1
        self.names = names
        # some information about the data,  needed later
        self.info = 'Data X, y'
        self.y_type = 'Full'   
        self.X_type = 'Full'

    def save_X(self):
        self.X_raw = self.X
        self.y_raw = self.y
        self.area_X_raw = self.area_X
        self.area_y_raw = self.area_y

    def re_initialise(self):
        """ Returns X and y back to initial state """
        self.__init__(self.X_raw, self.y_raw, self.names, self.lons, self.lats, self.lons1, self.lats1)
        self.area_X = self.area_X_raw
        self.area_y = self.area_y_raw
        if self.y_type == 'Reduced' :
            self.area_y = self.area_y_red

    def scale_X(self):
        scaler = StandardScaler()
        self.X = scaler.fit(X)
        self.info = self.info + '\nX scaled'

    def scale_y(self):
        scaler = StandardScaler()
        self.y = scaler.fit(y)
        self.info = self.info + '\ny scaled'

    def split_set(self, option):
        """ splits X and y into test and training data depending on 
        preferred option
        Currently,  options are either Inter for a choice of intermediate
        sized test runs (specific to names) 
        # EDIT THIS SO CAN CHOOSE TRAINIG RUNS HERE
        or Random_N where N is an integer that is used for the seed
        in train_test_split     """
        X = self.X
        y = self.y
        names = self.names
        if option == 'Inter':
            # Chosen so the test set are intermediate sized
            idx_train = list(range(0, 4))+list(range(5, 12))+[13]+list(range(16, 22))+[23, 25]
            idx_test = [4, 12, 14, 15, 22, 24]

            X_train, X_test = X[idx_train], X[idx_test]
            y_train, y_test = y[idx_train], y[idx_test]

        elif 'Random' in option:
            random_seed = int(option.split("_")[1])
            n_samples = len(names)
            idxs = np.arange(n_samples)
            X_train,  X_test,  y_train,  y_test,  idx_train,  idx_test = train_test_split(X,  y,  idxs,  test_size=0.2,  random_state=random_seed)
        elif option in names:
            print(option)
            idx_test = names.index(option)
            print(idx_test)
            idxs = list(range(len(names)))
            print(idxs)
            idx_train = [idx for idx in idxs if idx!=idx_test]
            idx_test = [idx_test]
            print(idx_train)
            X_train, X_test = X[idx_train], X[idx_test]
            y_train, y_test = y[idx_train], y[idx_test]

        training_runs = [names[idx] for idx in idx_train]
        test_runs = [names[idx] for idx in idx_test]

        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.training_runs = training_runs
        self.test_runs = test_runs
        self.info = self.info+' \nSplit into train and test data using %s option '%option

        return (X_train, X_test, y_train, y_test, training_runs, test_runs)



    def principal_components_X(self, no_of_components=None):
        pca = PCA(no_of_components)
        pca_trained = pca.fit(self.X_train)
        self.X_train = pca_trained.transform(self.X_train)
        self.X_test = pca_trained.transform(self.X_test)
        
        self.info = self.info + '\nPCA on X'
        self.X_type = 'PCA'

    def principal_components_y(self, no_of_components=None):
        pca_trained = PCA(no_of_components).fit(self.y_train)
        self.y_train = pca_trained.transform(self.y_train)
        self.y_test = pca_trained.transform(self.y_test)
        self.y_pca = pca_trained
        self.info = self.info + '\nPCA on y'
        self.y_type = 'PCA'

    def inverse_principal_components_y(self):
        pca_trained = self.y_pca
        self.y_pred = pca_trained.inverse_transform(self.y_pred)
        self.y_test = pca_trained.inverse_transform(self.y_test)

    def mean_y(self):
        y_mean = np.average(self.y, axis=1, weights=self.area_y)
        self.y = y_mean.reshape((len(y_mean), 1))
        self.y_type = 'Global mean'

    def mean_X(self):
        X_mean = np.average(self.X, axis=1, weights=self.area_X)
        self.X = X_mean.reshape((len(X_mean), 1))
        self.area_X = np.array([1.0])
        self.X_type = 'Global mean'

    def combine_X(self, X_add, X_area):
        self.X = np.concatenate((self.X, X_add), axis=1)
        self.area_X = np.concatenate((self.area_X, X_area))
        

    def regional_X(self, regions):
        # this should only be used if X is still the original X
        # add an error catcher here for if regional_X or mean_X etc. 
        # has been applied already- or if already split into training data
        X_regional = split_into_regions(self.X, self.area_X, 
                       self.lons, self.lats, self.lons1, self.lats1, 
                       regions)
        self.X = X_regional
        self.X_type = 'Regional'
        self.area_X = np.ones(len(regions))
        self.info = self.info + '\nRegional X'

    def regional_y(self, regions):
        print((self.y.shape))
        print(self.area_y.shape)
        y_regional = split_into_regions(self.y, self.area_y, 
                      self.lons, self.lats, self.lons1, self.lats1, 
                      regions)
        self.y = y_regional
        self.y_regions = regions
        self.area_y = np.ones(len(regions))
        self.y_type = 'Regional'
        self.info = self.info + '\nRegional y'

    def predict(self, reg_type='Ridge', cvfolds=2, alpha_list = None, normalize=False, 
                sample_weight=None, coefs=False):
        if alpha_list is None:
            alpha_list = np.logspace(-1, 6, 15)
        if coefs:
            y_pred, coef, alpha_params = Regression(self.X_train, self.y_train, self.X_test, self.y_test, 
                                                    reg_type, coefs=True, alpha_list = alpha_list, 
                                                    ReturnBestAlpha=True, cvfolds=cvfolds, normalize=normalize,
                                                    sample_weight=sample_weight)
            print("Returning coefficients")
            self.coef = coef
            
        else:
            y_pred, alpha_params = Regression(self.X_train, self.y_train, self.X_test, self.y_test, reg_type,
                                          coefs=False, alpha_list = alpha_list, ReturnBestAlpha=True,
                                          cvfolds=cvfolds, normalize=normalize, sample_weight=sample_weight)
        self.alpha_params = alpha_params
        self.y_pred = y_pred
        self.info = self.info + '\nPrediction done \nParameters: %s'%alpha_params

    def predict_regularise(self, reg_type='Ridge', cvfolds=2, alpha_list=None, normalize=False, sample_weight=None):
        self.predict(reg_type, cvfolds, alpha_list, normalize=normalize, sample_weight=sample_weight)
        alpha = self.alpha_params['alpha']
        ind = int(list(alpha_list).index(alpha))
        print('index', ind)
        print(type(ind))
        if ind == 0:
            min_a = 0.1*alpha
        else:
            min_a = alpha_list[ind-1]
        if ind == len(alpha_list)-1:
            max_a = 10.*alpha
        else:
            max_a = alpha_list[ind+1]
        new_alpha_list = np.linspace(min_a, max_a, 50)
        print(new_alpha_list)
        for i in range(10):
            self.predict(reg_type, cvfolds, new_alpha_list, normalize=normalize)
            new_alpha = self.alpha_params['alpha']
            if np.abs(new_alpha - alpha) < 0.1*alpha:
                print('Iterations done')
                break
            ind = int( list(new_alpha_list).index(new_alpha))
            print('index', ind)
            if ind == 0:
                min_a = 0.9*new_alpha
            else:
                min_a = new_alpha_list[ind-1]
            if ind == len(new_alpha_list)-1:
                max_a = 10.*new_alpha
            else:
                max_a = new_alpha_list[ind+1]
            new_alpha_list = np.linspace(min_a, max_a, 50)
            print(new_alpha_list)
        print('final alpha', new_alpha)



    def predictRF(self):
        y_pred=Regression(self.X_train, self.y_train, self.X_test, self.y_test, 'RandomForest', coefs=False)
        self.y_pred = y_pred
        self.info = self.info + '\nPrediction done with Random Forest'
        self.alpha_params = {'alpha':'None- Random Forest used'}

    def metrics_regional(self, savemetrics, regions = ['Global', 'NHML', 'Europe', 'Africa', 'North America', 'East Asia', 'India', 'South America', 'Arctic'], 
                         e_pred = None, y_test=None):
        RegionalMetrics(self.y_pred, self.y_test, regions, self.lons, self.lats, 
                        self.lons1, self.lats1,  self.training_runs, self.test_runs, 
                        savefolder = savemetrics , areas_flat = self.area_y)


    def plot_results(self, saveplots, y_pred=None, y_test=None):
        if y_pred is None:
            y_pred = self.y_pred
        if y_test is None:
            y_test = self.y_test
       # assert self.y_type is 'Full' 
        rmse = np.sqrt(np.average((y_test-y_pred)**2., axis=1, weights=self.area_y))
        PredictionPlot(y_test, y_pred, self.lons, self.lats,  self.training_runs,  self.test_runs,  saveplots, [rmse])




    def save_results(self, saveresults):
        # Save
        print("Saving ... ")
        nc_file = saveresults
        dataset = netCDF4.Dataset(nc_file,  'w', format='NETCDF4_CLASSIC')
        N_train, p = self.X_train.shape
        N_test, k = self.y_test.shape
        dataset.createDimension('input_dim', p)
        dataset.createDimension('output_dim', k)
        dataset.createDimension('N_train', N_train)
        dataset.createDimension('N_test', N_test)

        X_train_nc = dataset.createVariable('X_train', np.float64, ('N_train', 'input_dim'))
        X_train_nc[:, :] = self.X_train
        X_test_nc = dataset.createVariable('X_test', np.float64, ('N_test', 'input_dim'))
        X_test_nc[:, :] = self.X_test
        y_train_nc = dataset.createVariable('y_train', np.float64, ('N_train', 'output_dim'))
        y_train_nc[:, :] = self.y_train
        y_test_nc = dataset.createVariable('y_test', np.float64, ('N_test', 'output_dim'))
        y_test_nc[:, :] = self.y_test
        y_pred_nc = dataset.createVariable('y_pred', np.float64, ('N_test', 'output_dim'))
        y_pred_nc[:, :] = self.y_pred
        print("Saved as %s"%nc_file)

    def pickle_object(self, filename):
        print("Saving entire class as %s"%filename)
        pickle.dump(self, open(filename, 'wb') )
        
    def unpickle_object(self, filename):
        print("Retrieve entire class and return self")
        new_data=pickle.load(open(filename, 'rb'))
        return new_data

    def reduce(self, X, area, lons, lats, n_red_lon=None, n_red_lat=None):
        """ reduces variable X or y so fewer inputs- using only every 10th lon/lat.
        note this means 14 x 14 points = 196,  or every 5th lon/lat gives 784 points
        must be divisible by nlon and nlat!! 
        choose this parameter in n_red """
        if n_red_lon is None:
            n_red_lon = 8 # can be 2, 4, 6, 8 .. (multiple of 192)
        if n_red_lat is None:
            n_red_lat = 5 # can be 5, 10,  ... multiple of 145
        nlon, nlat = len(lons), len(lats)
        
        X_full = X.reshape((X.shape[0], nlat, nlon))
        X_red = X_full[:, ::n_red_lat, ::n_red_lon]
        X_red = X_red.reshape((X.shape[0], X_red.shape[1]*X_red.shape[2]))
        
        area_full = area.reshape((nlat, nlon))
        area_red = area_full[::n_red_lat, ::n_red_lon]
        area_red = area_red.flatten()

        return(X_red, area_red)
        
    def un_reduce(self, X_red, area_red, lons, lats, n_red_lon=None, n_red_lat=None):
        if n_red_lon is None:
            n_red_lon = 8
        if n_red_lat is None:
            n_red_lat = 5
        nlon, nlat = len(lons), len(lats)
        nlon_red, nlat_red = nlon/n_red_lon,  nlat/n_red_lat
        N = X_red.shape[0]
        X_red = X_red.reshape((N, nlat_red, nlon_red))
        area_red = area_red.reshape((nlat_red, nlon_red)) 
        X_full = np.zeros((N, nlat, nlon))
        area_full = np.zeros((nlat, nlon))
        for i in range(nlon/n_red_lon):
            for j in range(nlat/n_red_lat):
                area_full[(j)*n_red_lat:(j+1)*n_red_lat, (i)*n_red_lon:(i+1)*n_red_lon]=area_red[j, i]
                for n in range(N):
                    X_full[n, (j)*n_red_lat:(j+1)*n_red_lat, (i)*n_red_lon:(i+1)*n_red_lon]=X_red[n, j, i]        

        X_full = X_full.reshape((N, nlat*nlon))
        area_full = area_full.flatten()
        return(X_full, area_full)

    def setup(self, X_type, y_type, X_regions=None, y_regions = None, n_red_lon = None, n_red_lat=None):
        if X_type == 'Regional':
            self.regional_X(X_regions)
        elif X_type == 'Global mean':
            self.mean_X()
        elif X_type == 'Reduced':
            X_red, area_red = self.reduce(self.X, self.area_X, self.lons_X, self.lats_X, n_red_lon, n_red_lat)
            self.X = X_red
            self.area_X = area_red
       
        
        elif (X_type  != 'Full') and (X_type!='PCA'):
            print('X_type not chosen correctly')
            exit()

        if y_type == 'Regional':
            self.regional_y(y_regions)
        elif y_type == 'Global mean':
            self.mean_y()
        elif y_type == 'Reduced':
            y_red, area_red = self.reduce(self.y, self.area_y, self.lons, self.lats, n_red_lon, n_red_lat)
            self.y = y_red
            self.area_y = area_red
            self.area_y_red = area_red

        elif (y_type != 'Full') and (y_type != 'PCA'):
            print('y_type not chosen correctly')
            exit()

    def run(self, X_type, y_type, reg_type, option, X_regions=None, y_regions = None, nPCA=None, 
            cvfolds=2, alpha_list=None, n_red_lon=None, n_red_lat=None, normalize=False, 
            repeat_regularise=True, coefs=False,  sample_weight=None):
        self.split_set(option) 
        if X_type == 'PCA':
            self.principal_components_X(nPCA)
        if y_type == 'PCA':
            self.principal_components_y(nPCA)
        print('predict')
        print(self.area_y.shape)
        if repeat_regularise:
            print("Repeat CV regularisation")
            self.predict_regularise(reg_type, cvfolds, alpha_list, normalize, sample_weight=sample_weight)
        else:
            print("No repeated CV Regularisation")
            print("Return coefs?", coefs)
            self.predict(reg_type, cvfolds, alpha_list, normalize, coefs=coefs)
        
        # if necessary,  return to full y output
        if y_type == 'PCA':
            self.inverse_principal_components_y()
            self.y_type = 'Full'
        elif y_type == 'Reduced':
            y_full, area_full = self.un_reduce(np.concatenate((self.y_pred, self.y_test), axis=0), self.area_y_red, self.lons, self.lats, n_red_lon, n_red_lat)
            self.y_pred = y_full[:1]
            self.y_test = y_full[1:]
            #self.area_y_red = self.area_y
            self.area_y = area_full


    def runRF(self, option):
        self.split_set(option)
        self.principal_components_X(None)
        self.principal_components_y(None)
        self.predictRF()
        self.inverse_principal_components_y()
    

 
