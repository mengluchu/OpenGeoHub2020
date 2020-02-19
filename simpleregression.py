# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 10:25:20 2020

@author: lu000012
"""



# Regression Example With Boston Dataset: Standardized and Wider
from pandas import read_csv
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
# load dataset
dataframe = read_csv("C:/Users/Lu000012/Documents/files/GLOBAL_LUR/merged.csv")
dataframe= dataframe.dropna
dataframe.shape
# split into input (X) and output (Y) variables
list(dataframe.columns) 
clean = dataframe.filter(regex= 'ROAD|pop|TROPO|wind|temp|day').dropna().drop_duplicates()
X = clean.drop(columns =['day_value']).values
Y = clean['day_value'].values
 
# define wider model
def wider_model():
	# create model
	model = Sequential()
	model.add(Dense(69, input_dim=69, kernel_initializer='normal', activation='relu'))
	model.add(Dense(1, kernel_initializer='normal'))
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam')
	return model


def batchnorm_model():
    model = Sequential()
    model.add(Dense(69, input_dim=69, use_bias = False))
    model.add(layers.BatchNormalization())
    model.add(Activation("relu"))
    model.add(Dense(1, kernel_initializer='normal'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

epochs_num = 1 
# evaluate model with standardized dataset
estimators = []
estimators.append(('standardize', StandardScaler()))
estimators.append(('mlp', KerasRegressor(build_fn=batchnorm_model, epochs = epochs_num, batch_size = 5, verbose = 0)))
#estimators.append(('mlp', KerasRegressor(build_fn=wider_model, epochs = epochs_num, batch_size = 5, verbose = 0)))

pipeline = Pipeline(estimators)
kfold = KFold(n_splits=10)
results = cross_val_score(pipeline, X, Y, cv=kfold)
print("accuracy: %.2f (%.2f) MSE" % (results.mean(), results.std()))
 
# Regression Example With Boston Dataset: Standardized and Wider
 