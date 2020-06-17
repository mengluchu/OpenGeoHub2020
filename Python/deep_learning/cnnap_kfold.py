#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 16:19:38 2020

@author: menglu
"""
import keras
from keras import layers
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D
from sklearn.utils import shuffle
import matplotlib.pyplot as plt

from pandas import read_csv
import numpy as np

from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from keras import backend as K

road4 = np.load('/Users/menglu/Documents/Github/deep_learning/predictors/road4.npy')
road3 = np.load('/Users/menglu/Documents/Github/deep_learning/predictors/road3.npy')
road2 = np.load('/Users/menglu/Documents/Github/deep_learning/predictors/road2.npy')
road5 = np.load('/Users/menglu/Documents/Github/deep_learning/predictors/road5.npy')
road1 = np.load('/Users/menglu/Documents/Github/deep_learning/predictors/road1.npy')

road234=np.array(( road2,road3, road4, road5))
road234r.shape
 
plt.imshow(road234r[1,:,:,3])
plt.show() 
plt.imshow(road234[3,:,:,1])
plt.show() 


mal = [599,2225,2478,2504] # id of removed rasters
ap = read_csv('/Users/menglu/Documents/Github/deep_learning/airbase_oaq.csv')
ap.shape[0]-2634
ap = ap[:-3042]
ap = ap.drop(mal)
ap.shape
ap.dropna # no na same as ap
ap['country'].unique()

Y = ap['value_mean']


road234r = np.moveaxis(road234, 3, 0)
road234r = np.moveaxis(road234r, 1, -1) # channel last: ! be super careful about what array reshape mean, it is not the same as movng axis!!
# road234r, Y = shuffle(road234r, Y) Why shuffle results in nan?
 
Xtrainv =road234r[1:2300,:,:,:] # 2300 for training and validation, consisting of trainging and validation
Xtest =road234r[2300:,:,:,:]  #330 for testing, not going to touch
Ytrainv = Y[1:2300]
Ytest = Y[2300:]

 

# define
# kernal initializer is important!
def cnn_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same',
                 input_shape=input_shape, kernel_initializer = 'normal'))
    model.add(layers.BatchNormalization())
    model.add(Activation('relu'))
    
    model.add(Conv2D(32, (3, 3)))
    model.add(layers.BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

     
    
    model.add(Conv2D(32, (3, 3)))
    model.add(layers.BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    
   
    model.add(Activation('relu'))
    
    model.add(Flatten())
    model.add(Dense(1))
 
    model.add(Activation('relu'))
    return model
# I obtained higer accuracy with dropout and bachnorm. The mae is almost almost be around 10. 
# averagepooling is not as steady as maxpooling
# data augumentation assumes the inputs are images, with 1, 3, or 4 channels: grayscale, rgb, 
# the first dimension is always the number of samples. 

k  = 5 # fold
num_validation_samples = Xtrainv.shape[0]//k
validation_scores = []
for fold in range (k):
    validation_X= Xtrainv[num_validation_samples*fold : num_validation_samples*(fold+1),:,:,:]
    training_X = np.concatenate((Xtrainv[:num_validation_samples*fold,:,:,:] , Xtrainv[num_validation_samples*(fold+1):,:,:,:]),axis =0)
    validation_Y= Ytrainv[num_validation_samples*fold : num_validation_samples*(fold+1)]
    training_Y = np.concatenate((Ytrainv[:num_validation_samples*fold], Ytrainv[num_validation_samples*(fold+1):]),axis=None) 

    
    input_shape = (training_X.shape[1], training_X.shape[2], training_X.shape[3]) 
        
    m = cnn_model() 
    #print(cnn_model().summary())
    m.compile(loss='mae',
              optimizer='adam',
              metrics=['mse', 'mae'])

    
 
    history = m.fit(training_X, training_Y,
          batch_size= 50,
          epochs= 15,
          verbose=1,
          validation_data=(validation_X, validation_Y))
    validation_score =history.history['val_mae']
    validation_scores.append(validation_score)

validation_score =np.average(validation_scores)
testscore = m.evaluate(Xtest, Ytest, verbose=0)
print('val-:',validation_score, 'test:', testscore[0])
  
     
# "Loss"
   