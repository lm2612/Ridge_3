import FileCodesToName 
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_decomposition import PLSRegression
from sklearn.decomposition import PCA

def Regression(X_train, y_train, X_test, y_test, reg_type='Ridge', coefs=False, alpha_list = [1.0, 1.0e1, 1.0e2, 1.0e3, 1.0e4, 1.0e5], ReturnBestAlpha=False, cvfolds=2, normalize=False, sample_weight=None, n_jobs=1):
    """ Does the regression part based on X_train and y_train 
    and returns predicted y for X_test
    Choose type of regression,  eg. 'Ridge' or 'Lasso' or 'ElasticNet'
    Other parameters: number of times to do cross-validation, whether to normalise, """
    # Define parameters for the regression model for Ridge or
    # Lasso to train for different regularisation parameters alpha
    N, p = X_train.shape
    print(alpha_list)
    parameters = { 'alpha': alpha_list, 
                'fit_intercept': [True],  
                'max_iter':[1000], 
                'tol': [0.0001], 
                'normalize':[normalize] }

    if reg_type == 'Ridge':
        regr_model = Ridge()
    elif reg_type == 'Lasso':
        regr_model = Lasso()
    elif reg_type == 'ElasticNet':
        regr_model = ElasticNet()
        
    regr = GridSearchCV(regr_model, parameters, cv=cvfolds, n_jobs=n_jobs, refit=True,
                            scoring='neg_mean_squared_error')
    regr.fit(X_train, y_train, sample_weight)
    
    y_pred_test = regr.best_estimator_.predict(X_test)
    print('best params = ', regr.best_params_)


    if coefs is True:
        # Return weights for regression as well (default is False)
        best_regr = regr.best_estimator_
        coef = best_regr.coef_
        if ReturnBestAlpha is True:
            return y_pred_test, coef, regr.best_params_
        else:
            return y_pred_test, coef
        
    elif ReturnBestAlpha is True:
         return y_pred_test, regr.best_params_
    
    else:
        return y_pred_test


