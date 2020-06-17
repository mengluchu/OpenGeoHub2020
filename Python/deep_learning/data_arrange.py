#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:25:25 2020

@author: menglu
"""

import os
import gdal 
import numpy as np

 
import pandas as pd
os.getcwd()
directoryPath = os.path.join(directoryPath, directoryName)
os.chdir("/Volumes/Seagate Expansion Drive" )
le = len( os.listdir(rasterdir ) )
rasterdir = "/Volumes/Seagate Expansion Drive/global"
def crop_center(img,cropx,cropy):
    y,x = img.shape
    startx = x//2 - cropx//2
    starty = y//2 - cropy//2    
    return img[starty:starty+cropy, startx:startx+cropx]

result= np.empty([32, 32])
j = 0 
mal = []
for i in range(1,2634):
    mapdir = os.path.join(rasterdir,str(i),"laea","road_class_3_25.map")
   # os.chdir(os.path.join(rasterdir,str(i),"laea"))
       
    arr = np.array(gdal.Open(mapdir).ReadAsArray()   )
    if arr.shape[1] < 32:
        print (i)
        mal2  = i
        mal.append(mal2)
        continue
    arr = crop_center(arr, 32,32)
    result = np.dstack((result,arr))
   # plt.imshow(arr)
   # plt.show()
   # print(arr.shape)
np.save('/Users/menglu/Documents/Github/deep_learning/predictors/road4', result)
np.save('/Users/menglu/Documents/Github/deep_learning/predictors/road2', result)
np.save('/Users/menglu/Documents/Github/deep_learning/predictors/road3', result)
#599,2225,2478,2504
# till 2634




