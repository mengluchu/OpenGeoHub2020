## Introduction

In many middle and low-income countries, air pollution monitor networks are deficient or nonexisting, but in these countries people are the most vulnerable to air pollution, with young children suffer the most. The idea is to borrow information from countries where relatively dense ground monitors are available, and integrate information from satellite measurements and geospatial predictors, to give an estimation of global air quality. The challenge lies in modelling the geospatially heterogenious relationships between predictors and pollutants, as well as integrating remote sensing measurements and predictors from different resolutions and sources. Machine learning methods, when making full use of spatial information, clearly is an auspicious shot. 

In this course, I will introduce the whole global air pollution modelling process, with a focus on introducing how different machine learning (regularized regression, ensemble trees, deep learning) can be used in spatial NO2 prediction. The deep learning and variable predictor calculations are introduced in Python and others in R. I will also briefly go through the convenient features of these two languages, many developments try to combine them in one environment, which will take time to see if it is the most efficient way. I am an R user for almost 10 years and in these 3 years gradually becoming also fond of Python.  

Deep learning is a very fast evolving and facinating fields, many strategies, architectures, concepts have been developed. You may learn in the workshop that it is a powerful representation learning tool that is a game changer in computer vision, which means also in many areas of remote sensing, particulaly in instance segmentation, localization, image maching, showing its great power in the era of big data. What about deep learning in air pollution mapping? The buergeoning data and algorithms may provide us an unprecedented opportunity.

**After this course, you will 1) learn a variety of machine learning algorithms; 2) become an efficient modeller; 3) understand/implement/use the newest algorithms in machine learning and (hopefully) also be interested in challenges in global prediction problems**.

## Methods to be learned are: 
- **Model Regularization** (Ridge; Lasso; Elastic Net; XGBoost, Deep Neural Networks)
- **Random Forest**
- **Boosting** (e.g. gradient boosting machine and XGBoost)
- **Deep Neural Networks** 
  - point-based
  - convolutional neural networks: Self-defined and recently development 
- **Mixed effect models 

## Course Material:
### The *R_script* folder 
contains 4 sub-folders: 
 

- Data Visualize: visualizing Satellite imagery and the OpenAQ API.
  - **plot_RS.Rmd**: visualize the 3 remote sensing products.
  - **openaq.Rmd** : querying open openaq data using R API 

- Introduction
  - **Geohub_2020.Rmd**: data analysis script that includes a variety of tools for data exploration and modeling. You can explore the data and analyse modeling results, for example looking at the scatterplots, spatial correlations, partial dependence plot, importance plot. You can also see how the machine learning functions are parameterized and used for modelling, besides the deep neural networks, which is implemented in Python. 

- modeling_process: the modelling process from hyperparameter optimization, cross validation, to mapping.

  - **Glo_hyp_tun.Rmb**: hyperparmeter tunning for the xgboost, random forest, and gradient boosting machine, using grid search and R caret package.
  - **Glo_vali_map_compare** : the models are validated using bootstrapping (eval set to false, if you want to try it to yourself it takes about 10 minutes), the variable importance are averaged over the bootstrapped rounds. The models are used to make predictions (map) in a small region. The prediction results are further compared with mobile sensor measurements (air monitor stations on board a carrier-bike).

- Others: Consists of small experiements to deepen the understandings of Machine learning.
  - **differences between ML and statistics**
  - **ensemble**: ensemble multiple machine learning models, which often could give the best results.

### The *Python* folder
The predictor calculation and deep learning are implemented in Python, due to some benefits over R -- some tools are currently only developed in Python, and most people in the deep learning community use python. In this folder there is a note about how to start using conda environment for people new to python.   

This folder contains two subfolders:

- deep learning
  two methods are implemented: point-based and convolutional based. Please go to the folder for more info. 
  
- calc_predictors
  In this study, we used buffered variables -- variables aggregated over buffers of various sizes. The roads and industry variables are calcualted from OpenStreetMap. Scripts to downloading OpenStreetMap data, pre-processing, and calculate buffers are included in this folder. Please refer to the README file in the foler for more details. You can also visit our GitHub page to reproduce all the predictor variables, or calculate your own predictors. I believe this will greatly faciliate relevant research, especially studies starting from scratch. 
 
### Other folders:
  - **slides**: the slides for the plenary and workshop in the afternoon
  - **output**: some output saved from running the Geohub.Rmd
  - **rasters**: remote sensing products and a 1 degree by 1 degree tile of all the predictors for mapping and visual inspection.
 
