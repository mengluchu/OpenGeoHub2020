## Introduction

In many middle and low-income countries, air pollution monitor networks are deficient or nonexisting, but in these countries people are the most vulnerable to air pollution, with young children suffer the most. The goal is to integrate information from ground station measurements, satellite measurements and geospatial predictors, to estimate global air quality, at a high resolution (< 100 m). Challenges are:
1. Modelling the geospatially heterogenious relationships between predictors and pollutants. 
2. Assimilating Geospatial predictors, ground sensor and satellite instruments measured pollutants from various resolutions and sources.
3. Modelling the effects of transportation network structures (to air pollutant emission). 

With geospatial predictors and measurements growing in spatiotemporal resolution, coverage, and diversity, machine learning algorithms (statistical- based methods) provide an unprecedented opportunity to map our environment. Many atmospheric numerical modellers are impressed by the accuracy a statistical model could reach, however, global high-resolution air quality mapping is still at its infacy, the chanllenges are awaiting to be addressed.    

In this course, I will introduce most recent status in global air pollution modelling, with a focus on introducing different machine learning algorithms (e.g. ensemble trees, deep learning) and strategies (e.g. regularization, postprocessing). The deep learning and variable predictor calculations (in particular OpenStreetMap querying and processing), are introduced in Python and others in R. For the Python part, a [Kaggle notebook](https://www.kaggle.com/notebooks) is shared, meaning nothing needs to be installed or computed locally.

Deep convolutional neural networks are a powerful representation learning tool that is a game changer in computer vision. Can it also be used to extract more complex features from our transportation networks0 for better air pollution mapping and help with finding the road network-air pollution relationships?

**After this course, you can expect to 1) understand the current challenges in global environmental mapping (prediction) and methods to approach them, 2) Learn a variety of machine learning algorithms, and 3) Be able to apply the most recent and powerful algorithms in practice. 

## Methods to be learned are: 
- **Random Forest**
- **Boosting** (e.g. gradient boosting machine and XGBoost)
- **Model Regularization and postprocessing** 
- **Deep Neural Networks** 
  - point-based
  - convolutional neural networks apply to OpenStreetMaps
- **Mixed-effect models** 

## Course Material:
### The  [R_scripts](/R_scripts/) folder 
contains 5 sub-folders that corresponds to the Introduction, statistical method, and modeling process sections of the lecture: 
 

- [Data_visualize](/R_scripts/Data_visualize/): visualizing Satellite imagery and the OpenAQ API.
  - **plot_RS.Rmd**: visualize the 3 remote sensing products.
  - **openaq.Rmd** : querying open openaq data using R API 
  - **rasters**: remote sensing products and a 1 degree by 1 degree tile of all the predictors for mapping and visual inspection

- [Introduction](/R_scripts/Introduction/)
  - **Geohub_2020.Rmd**: data analysis script that includes a variety of tools for data exploration and modeling. You can explore the data and analyse modeling results, for example looking at the scatterplots, spatial correlations, partial dependence plot, importance plot. You can also see how the machine learning functions are parameterized and used for modelling, besides the deep neural networks, which is implemented in Python. 
  - **shiny_randomforest** and **shiny_xgboost**: R shiny apps developed to provide an intuitive understanding of the effects of hyperparameters on the prediction patterns, instead of only focusing on the cross-validation. [For XGboost it can be viewed here](https://lumeng0312.shinyapps.io/xgboost/?_ga=2.179522658.79817579.1592385947-986486774.1592216474), and [a comment here](https://tomatofox.wordpress.com/2020/06/15/hyperparameters-of-ensemble-trees/).

- [convolution_filter](/R_scripts/convolution_filter/)
  - **convolutional illustrated.Rmd**: Basic image analysis: the effect of different convolutional filters in image edge extraction, sharpening and blurring. 
 
- [modeling_process](/R_scripts/modeling_process/): the modelling process from hyperparameter optimization, cross validation, to mapping.

  - **Glo_hyp_tun.Rmd**: hyperparmeter tunning for the xgboost, random forest, and gradient boosting machine, using grid search and R caret package.
  - **Glo_crossvali.Rmd** : the models are validated using bootstrapping (eval set to false, if you want to try it to yourself it takes about 10 minutes), the variable importance are averaged over the bootstrapped rounds. 
  - **Glo_map.Rmd**: The models are used to make predictions (map) in a small region, using multiple methods for comparison.  
  - **dc.gri, dc.grd**: Geospatial predictors used for mapping.

- [other](/R_scripts/other/): Consists of small experiements to deepen the understandings of Machine learning.
  - **differences between ML and statistics**
  - **ensemble**: ensemble multiple machine learning models, which often could give the best results.

### The [Python](/Python/) folder

The predictor calculation- in particular OSM map querying and buffer calculation, and deep learning process are implemented in Python, forming the last part of the workshop. Python is used as some tools are currently only developed in Python, and most people in the deep learning community use python, contributing to (in my opinion) a faster pacing development. In this folder there is a note about how to start using conda environment for people new to python.   

This folder contains:

- [deep_learning](/Python/deep_learning/)
  two methods are implemented: point-based and convolutional based. Please go to the folder for more info. 
  
- [calc_predictors](/Python/calc_predictors/)
  In this study, we used buffered variables -- variables aggregated over buffers of various sizes. The roads and industry variables are calcualted from OpenStreetMap. Scripts to downloading OpenStreetMap data, pre-processing, and calculate buffers are included in this folder. Please refer to the README file in the foler for more details. You can also visit our GitHub page to reproduce all the predictor variables, or calculate your own predictors. I believe this will greatly faciliate relevant research, especially studies starting from scratch. 

- [Notes for installing Anaconda and editor (Jupyter or Spyder)](/Python/README.md) 
 
### The [slides_notes](/slides_and_notes/) folder

the slides for the plenary and workshop in the afternoon. Software for querying and processing OpenStreetMap, and data description of the night earth light measurements.  


   
