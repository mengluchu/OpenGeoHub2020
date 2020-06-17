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
road234.shape
 
plt.imshow(road2[:,:,1])
plt.show() 


mal = [599,2225,2478,2504] # id of removed rasters
ap = read_csv('/Users/menglu/Documents/Github/deep_learning/airbase_oaq.csv')
ap.shape[0]-2634
ap = ap[:-3042]
ap = ap.drop(mal)
ap.shape
ap.dropna # no na same as ap
Y = ap['value_mean']

Xtrain =road234[:,:,:,1:2000]
Xtest =road234[:,:,:,2001:]
Ytrain = Y[1:2000]
Ytest = Y[2001:]

 
Xtrain = np.moveaxis(Xtrain, 3, 0)
Xtrain = np.moveaxis(Xtrain, 1, -1) # channel last: ! be super careful about what array reshape mean, it is not the same as movng axis!!

Xtest = np.moveaxis(Xtest, 3, 0)
Xtest = np.moveaxis(Xtest, 1, -1) # channel last: ! be super careful about what array reshape mean, it is not the same as movng axis!!

 

input_shape = (32, 32, 4) 


 
data_augmentation = False

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

    
Xtrain.shape
m = cnn_model() 
print(cnn_model().summary())
m.compile(loss='mse',
              optimizer='adam',
              metrics=['mse', 'mae'])

if not data_augmentation:
    print('Not using data augmentation.')
    
 
    history = m.fit(Xtrain, Ytrain,
          batch_size= 100,
          epochs= 15,
          verbose=1,
          validation_data=(Xtest, Ytest))
    score =m.evaluate(Xtest, Ytest, verbose=0)
    print('mse:', score[0])
  
    print(history.history.keys())
# "Loss"
    plt.plot(history.history['mae'])
    plt.plot(history.history['val_mae'])
    plt.title('model mae')
    plt.ylabel('mae')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
# save before show(), otherwise wont work
    plt.savefig("/Users/menglu/Documents/deep_learning/apcnn50poc_mae.png")
    plt.show()
else:
    print('Using real-time data augmentation.')
    # This will do preprocessing and realtime data augmentation:
    datagen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        zca_epsilon=1e-06,  # epsilon for ZCA whitening
        rotation_range=180,  # randomly rotate images in the range (degrees, 0 to 180)
        # randomly shift images horizontally (fraction of total width)
        width_shift_range=0.01,
        # randomly shift images vertically (fraction of total height)
        height_shift_range=0.01,
        shear_range=0.,  # set range for random shear
        zoom_range=0.,  # set range for random zoom
        channel_shift_range=0.,  # set range for random channel shifts
        # set mode for filling points outside the input boundaries
        fill_mode='nearest',
        cval=0.,  # value used for fill_mode = "constant"
        horizontal_flip=True,  # randomly flip images
        vertical_flip=True,  # randomly flip images
        # set rescaling factor (applied before any other transformation)
        rescale=None,
        # set function that will be applied on each input
        preprocessing_function=None,
        # image data format, either "channels_first" or "channels_last"
        data_format=None,
        # fraction of images reserved for validation (strictly between 0 and 1)
        validation_split=0.0)

    # Compute quantities required for feature-wise normalization
    # (std, mean, and principal components if ZCA whitening is applied).
    datagen.fit(Xtrain)

    # Fit the model on the batches generated by datagen.flow().
    history = m.fit_generator(datagen.flow(Xtrain, Ytrain,
                                     batch_size= 100),
                        epochs=5,
                        validation_data=(Xtest, Ytest),
                        workers=4)
    
    score =m.evaluate(Xtest, Ytest, verbose=0)
    print('mse:', score[0])
  
    print(history.history.keys())
# "Loss"
    plt.plot(history.history['mae'])
    plt.plot(history.history['val_mae'])
    plt.title('model mae')
    plt.ylabel('mae')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
# save before show(), otherwise wont work
    plt.savefig("/Users/menglu/Documents/Github/deep_learnings/apcnn50poc_mae.png")
    plt.show()

#Xnew = np.array([[40, 0, 26, 9000, 8000]])
#Xnew= scaler_x.transform(Xnew)
#ynew= model.predict(Xnew)
#invert normalize
#ynew = scaler_y.inverse_transform(ynew) 
#Xnew = scaler_x.inverse_transform(Xnew)
#print("X=%s, Predicted=%s" % (Xnew[0], ynew[0]))
#Xnew = np.array([[40, 0, 26, 9000, 8000]])
#Xnew= scaler_x.transform(Xnew)
#ynew= model.predict(Xnew)
#invert normalize
#ynew = scaler_y.inverse_transform(ynew) 
#Xnew = scaler_x.inverse_transform(Xnew)
#print("X=%s, Predicted=%s" % (Xnew[0], ynew[0]))