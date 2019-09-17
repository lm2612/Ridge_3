from sklearn.dummy import DummyRegressor
from PredictionData import * 

def DummyPrediction(X_train,y_train,X_test,y_test):
    dummy = DummyRegressor()
    dummy = dummy.fit(X_train,y_train)
    y_pred = dummy.predict(X_test)
    return(y_pred)

def AllDummyPrediction(option,X,y,names,lons,lats,lons1,lats1):
    d = PredictionData(X,y,names,lons,lats,lons1,lats1)
    d.info = 'Dummy regression'
    (X_train,X_test,y_train,y_test,training_runs,test_runs)  = d.split_set(option)
    y_pred = DummyPrediction(X_train,y_train,X_test,y_test)
    d.y_pred = y_pred
    return(d)
    
