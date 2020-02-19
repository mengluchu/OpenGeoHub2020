In many middle and low-income countries, air pollution monitor networks are deficient or nonexisting, but in these countries people are the most vulnerable to air pollution, with young children suffer the most. The idea is to borrow information from countries where relatively dense ground monitors are available, and integrate information from satellite measurements and geospatial predictors, to give an estimation of global air quality. The challenge lies in the geospatially heterogenious relationships between predictors and pollutants, as well as integrating remote sensing measurements and predictors from different resolutions and sources. Machine learning methods, augumented with spatiotemporal information, may provide flexible models to partially solve these problems. 

In this course, I will introduce different machine learning (regularized regression, ensemble trees, deep learning) and how they can be used in spatial NO2 prediction. The deep learning is in Python and others in R. I will also briefly go through the convenient features of these two languages, many developments try to combine them in one environment (I think better to develop on both, but learning from each other for improvements). I am an R user for more than 8 years and in these 3 years gradually moving some of my works to Python (I actually like it better, and I got the feeling that even the statistical community of Python is catching up).   

Deep learning is a very fast evolving and facinating fields, and the many strategies developed there can be adaped to ensemble learning methods. (This representation learning tool, showing its power in the era of big data, is actually not suitable for this air pollution prediction, considering the number of ground observations.)  

The methods will be 
- **Ridge**
- **Lasso**
- **Elastic Net**
- **random forest**
- **gradient boosting machine**
- **xgboost**
- **Neural Networks**


The **Geohub.Rmd** file is the data analysis script that is used for the workshop. The **plot_RS.Rmd** shows the 3 remote sensing products. 

Folders:
- **slides**: the slides for the plenary and workshop in the afternoon
- **output**: some output saved from running the Geohub.Rmd
- **predict_tiles**: functions and dataset for making predictions (mapping) in a (10km by 10km) example region.
- **Satelite**: the remote sensing products
