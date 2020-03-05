# Geospatial predictor calculation


Scripts to calculate predictor variables, particularly buffered variables, and other preprocessing scripts. 


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

## Detailed steps
  1. Check current osm file from planet.openstreetmap.org/pbf, edit the get_pbf.sh for the newest osm. 
  2. Run sh get_pbf.sh, the file will be downloaded to the current directory, the file is 50 G, for the global dataset. If you want to try a smaller area, e.g. by country, you may find it from geofabrik.
  3. Set the osm directory in landuse.py and road.py, run the scripts. This will extract elements from the osm map. 
  4. In "setting.py", set the directory for osm gpkg file for road and industrial areas (data_source). Also, set the directory for the results. You can also set the cpus to calculate buffers, the road classes (road_classes) and the buffer sizes (road_buffersizes). You can set the parameter "cellsize" (in meters) for the resolution, radius_x (in degree) and radius y (in degree) for the extent of the map. The radius_x and radius_y are the halfside of the rectangular, in degree. For example, if you set radius_x = 0.1and radius_y = 0.1, the result will be roughly in a 10 km by 10 km tile. The "halo_x" (in degree) is to give an extended area for boarder pixels. If you want to calculate a 5 km buffer for each pixel, then the halo_x should be roughly 0.006
  5. Set the prediction centre in centre.csv file (longitude, latitude)
  6. Run the predictor.py file


## Details
  * For each centre, the input data will be considered as in wgs84 geographical coordinate system (EPSG:4326). Based on the projection centre coordinates, the input will be projected using the lamba equal distance conic projection: "EPSG:4326 -t_srs "+proj=laea +lon_0={} +lat_0={} +R=0 +x_0=0 +y_0=0 +units=m +no_defs"
  


## Note
* Openstreetmap is a valuable data source and so far the most comprehensive for road networks. However, the infomation it contains is massive and somewhat messy. More importantly, the information is unequal over the globe. This part of bias should be well accounted when using openstreetmap for global mapping.

* Calculating the predictors globally, at 25 m resolution requires supercomputation, or you may try using google earth engine, which may be the best way if you don't have many cpu cores. But at 100m resolution is probabaly doable at a local machine. 25 m resolution mapping can provide more opportunities for understanding road effects, but the bias from openstreetmap, as well as the number of ground monitors that are established close to roads, should be considered.  

* This calculation uses pcraster software, for the setup, please refer to the pcraster installation website, http://pcraster.geo.uu.nl/quick-start-guide/, which should be simple but is python-version-dependent:
1. create a conda environment
2. check the pcraster version, which python version it is built on:
  * conda create --name predictors python=3.7
  * conda activate predictors (replace predictors with your environment name)
  * conda install GDAL 
  * conda install -c http://pcraster.geo.uu.nl/pcraster/pcraster -c conda-forge pcraster=4.3.0_rc1 

* note：
  * install GDAL before pcraster to avoid conflictions.
  * if you use a conda environment you dont need to export the pythonpath, because everything is in the environment (use vi ~/.bashrc to manage, you may need to remove previously exported path).  

* Any suggestions and critisms are welcomed! 

## Acknowledgement
The process was developed by the research group at global geo health data centre (Meng Lu, Derek Karssenberg, Oliver Schmitz). Most credits are given to Dr. Oliver Schmitz, who is the author of the scripts and implemented the workflow. 
