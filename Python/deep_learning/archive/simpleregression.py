 
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 10:25:20 2020

@author: lu000012
"""



# Regression with the global air pollution dataset, only from a single pixel of a set of variables to a value (point -> point)
# try batch normalization and without batch normalization and different model structures.
from pandas import read_csv
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras import layers
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn import preprocessing
# load dataset
dataframe = read_csv("/data/lu01/merged.csv")

# split into input (X) and output (Y) variables

clean = dataframe.filter(regex= 'ROAD|pop|TROPO|wind|temp|day').dropna().drop_duplicates()


X = clean.drop(columns =['day_value']).values # remove observations
Y = clean['day_value'].values # df to array
#X = preprocessing.normalize(X) # important: normalize to zero mean and sd = 1, will do later 
# define wider model
def wider_model():
	# create model
	model = Sequential()
	model.add(Dense(59,  kernel_initializer='normal', activation='relu'))
        model.add(Dense(29,  kernel_initializer='normal', activation='relu'))
        model.add(Dense(19,  kernel_initializer='normal', activation='relu'))
	model.add(Dense(1, kernel_initializer='normal'))
	# Compile model
	model.compile(loss='squared_error', optimizer='adam')
	return model


def batchnorm_model():
    model = Sequential()
    model.add(Dense(20, use_bias = False)) #default batch = 32， bias no longer needed
    #model.add(layers.Dropout(0.3))
    model.add(layers.BatchNormalization()) # no need to batch norm or use a low dropout
    model.add(Activation("relu"))
    
    model.add(Dense(10, use_bias = False)) #default batch = 32， bias no longer needed
  
    model.add(layers.BatchNormalization())
    model.add(Activation("relu"))
  
    model.add(Dense(1, kernel_initializer='normal'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

def vis_model(X):
    model = Sequential()
    model.add(Dense(20, use_bias = False, input_shape = (X.shape[1],))) #default batch = 32， bias no longer needed
    #model.add(layers.Dropout(0.3))
    model.add(layers.BatchNormalization()) # no need to batch norm or use a low dropout
    model.add(Activation("relu"))
    
    model.add(Dense(10, use_bias = False)) #default batch = 32， bias no longer needed
  
    model.add(layers.BatchNormalization())
    model.add(Activation("relu"))
  
    model.add(Dense(1, kernel_initializer='normal'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    
    return model
 
m = vis_model(X)
m.summary()
 

epochs_num = 150
# not standardize
estimators = KerasRegressor(build_fn=batchnorm_model, epochs = epochs_num, batch_size = 100, verbose = 1)
kfold = KFold(n_splits=10)
results = cross_val_score(pipeline, X, Y, cv=kfold, scoring = "r2")
print("accuracy: %.2f (%.2f) R2" % (results.mean(), results.std()))
 
 
# evaluate model with standardized dataset
estimators = []
estimators.append(('standardize', StandardScaler())) # normalize here
estimators.append(('mlp', KerasRegressor(build_fn=batchnorm_model, epochs = epochs_num, batch_size = 100, verbose = 1)))
#estimators.append(('mlp', KerasRegressor(build_fn=wider_model, epochs = epochs_num, batch_size = 5, verbose = 0)))

pipeline = Pipeline(estimators)
kfold = KFold(n_splits=20)
results = cross_val_score(pipeline, X, Y, cv=kfold, scoring = "r2")
print("accuracy: %.2f (%.2f) R2" % (results.mean(), results.std()))

# Regression Example With Boston Dataset: Standardized and Wider
 #-162.44 (39.54) MSE, -148.97 (30.97) MSE
