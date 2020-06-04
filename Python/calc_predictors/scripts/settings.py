import os

# Make sure this directory exists, will not be created
result_dir = os.path.join('/', 'data', 'results', 'global')


gdal_path = '' #os.path.join(os.environ['HOME'], 'miniconda3', 'envs', 'pcraster421', 'bin')
pcraster_path = '' #os.path.join('/', 'opt', 'pcraster', '20190519', 'bin')

path_ogr2ogr = os.path.join(gdal_path, 'ogr2ogr')
path_gdal_rasterize = os.path.join(gdal_path, 'gdal_rasterize')
path_gdalwarp = os.path.join(gdal_path, 'gdalwarp')
path_gdal_translate = os.path.join(gdal_path, 'gdal_translate')

path_map2col = os.path.join(pcraster_path, 'map2col')
path_col2map = os.path.join(pcraster_path, 'col2map')
path_resample = os.path.join(pcraster_path, 'resample')


industry_source = os.path.join('/', 'data', 'gghdc','data', 'data_2019','gap_industrial.gpkg')
data_sources = os.path.join('/', 'data', 'gghdc','data', 'data_2019')


road_sources = data_sources

path_python_exe = 'python3'

coord_centre = os.path.join('/', 'data', 'lu01', 'predictors', 'scripts', 'airbase_oaqcoords.csv')
buffer_cpus = 4
road_classes = [1, 2, 3, 4, 5]
road_buffersizes = [25, 50, 100, 300, 500, 800, 1000, 3000, 5000]


cellsize = 100.0 # in m, can put higher value for testing
radius_x = 0.5 # degree, half side of the square
radius_y = 0.5
halo_x = 0.06 # 5km for the boarder
 



