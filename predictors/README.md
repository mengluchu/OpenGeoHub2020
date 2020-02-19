# Global Air Pollution mapping with LUR models



Private repository containing scripts to calculate predictor variables, and other preprocessing scripts.


Contents of folder (and order of execution):

## Data preprocessing

In the preprocessing/openstreetmap folder:

  1. data: Script to obtain the OpenStreetMap dataset

  2. landuse: Script to generate the industry class land use map

  3. roads: Script to generate the individual road class datasets

## Calculating the predictor variables

You might need to adapt path locations etc.

  * centres.csv: Locations that will be calculated

  * clean.py: Script to remove directories

  * make_buffer.py: Script to calculate the buffers. Do not edit

  * settings.py: Script with path locations and buffer sizes to calculate

  * predictors.py: Script to calculate the predictors for each location


## Required software

  * PCRaster 4.2 or higher

  * Python 3 with Numpy and GDAL modules

