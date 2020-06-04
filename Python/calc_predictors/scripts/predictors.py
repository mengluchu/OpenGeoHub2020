# skip buffer calculation when maptotal is 0
# can we VectorTranslate to a layer directly
# check resample/conversion to tiff, reduce that

import glob
import numpy
import datetime
import sys
from osgeo import gdal
from osgeo import ogr
from osgeo import osr

from pcraster import *
from pcraster.framework import *

import settings

if int(gdal.VersionInfo('VERSION_NUM')) < 2000000:
    raise RuntimeError('Python bindings of GDAL 2.x or later required!')

class GdalErrorHandler(object):
    def __init__(self):
        self.err_level=gdal.CE_None
        self.err_no=0
        self.err_msg=''

    def handler(self, err_level, err_no, err_msg):
        self.err_level=err_level
        self.err_no=err_no
        self.err_msg=err_msg


err=GdalErrorHandler()
handler=err.handler
gdal.PushErrorHandler(handler)
gdal.UseExceptions()


class CalcPredictor(StaticModel, MonteCarloModel):
  def __init__(self, cellsize, buffersizes, halo_size, industry_source, road_sources, road_classes, radius_x, radius_y, halo_x, halo_y, result_dir):
    StaticModel.__init__(self)
    MonteCarloModel.__init__(self)
    # Just create a clone to satisfy modelling framework
    setclone(1, 1, 1, 1, 1)


    self.longitude = None
    self.latitude = None
    self.area_id = None
    self.result_dir = result_dir

    # Bounding box in degrees
    self.radius_x = radius_x
    self.radius_y = radius_y
    self.halo_x = halo_x
    self.halo_y = halo_y

    # Raster, in metres
    self.halo_size = halo_size
    self.cellsize = cellsize
    self.buffer_sizes = buffersizes

    self.industry_source = industry_source
    self.road_sources = road_sources
    self.road_classes = road_classes


  def postmcloop(self):
    pass

  def premcloop(self):
    self.omi_centres = numpy.loadtxt(settings.coord_centre, delimiter=',')


  def make_directories(self):
    # Create subdirectories per CRS
    dirname = os.path.join(str(self.currentSampleNumber()), 'wgs84')
    os.makedirs(dirname, exist_ok=True)
    assert os.path.exists(dirname) and os.path.isdir(dirname)

    dirname = os.path.join(str(self.currentSampleNumber()), 'laea')
    os.makedirs(dirname, exist_ok=True)
    assert os.path.exists(dirname) and os.path.isdir(dirname)





  def make_wgs84_point(self):
    # Create GeoPackage with all the required layers; in WGS84

    path = os.path.join(str(self.currentSampleNumber()), 'wgs84', 'wgs84.gpkg')

    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromEPSG(4326)

    ds = ogr.GetDriverByName('GPKG').CreateDataSource(path)

    lyr = ds.CreateLayer('centre', geom_type=ogr.wkbPoint, srs=spatial_ref)

    lyr.CreateField(ogr.FieldDefn('centre_id', ogr.OFTInteger))

    feat = ogr.Feature(lyr.GetLayerDefn())
    feat['centre_id'] = self.area_id

    feat.SetGeometry(ogr.CreateGeometryFromWkt('POINT({} {})'.format(self.longitude, self.latitude)))

    lyr.CreateFeature(feat)

    feat = None
    lyr = None
    ds = None



  def make_wgs84_box(self, layername, radius_x, radius_y=None):
    # Add bounding boxes (matching OMI cells)
    if radius_y is None:
      radius_y = radius_x

    path = os.path.join(str(self.currentSampleNumber()), 'wgs84', 'wgs84.gpkg')

    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromEPSG(4326)

    ds = ogr.GetDriverByName('GPKG').Open(path, update=1)
    lyr = ds.CreateLayer(layername, geom_type=ogr.wkbPolygon,  srs=spatial_ref)

    feat = ogr.Feature(lyr.GetLayerDefn())

    ring = ogr.Geometry(ogr.wkbLinearRing)

    ring.AddPoint(self.longitude - radius_x, self.latitude + radius_y)
    ring.AddPoint(self.longitude + radius_x, self.latitude + radius_y)
    ring.AddPoint(self.longitude + radius_x, self.latitude - radius_y)
    ring.AddPoint(self.longitude - radius_x, self.latitude - radius_y)
    ring.AddPoint(self.longitude - radius_x, self.latitude + radius_y)

    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)


    feat.SetGeometry(poly)
    lyr.CreateFeature(feat)

    feat = None
    lyr = None



  def clip_wgs(self, source, source_layer_name, clip_layer_name, dest_layer_name, dest_layer_type):

    # First do a spatial filtering on the source dataset
    # creates full subset of the area (all layers)
    src_ds = gdal.OpenEx(source)

    ofile = os.path.join(str(self.currentSampleNumber()), 'wgs84', 'tmp_{}.gpkg'.format(dest_layer_name))
    spatial_filter_area = [self.longitude - self.radius_x - 0.1, self.latitude - self.radius_y - 0.1, self.longitude + self.radius_x + 0.1, self.latitude + self.radius_y +0.1]
    ds_out = gdal.VectorTranslate(ofile, src_ds, format = 'GPKG', spatFilter = spatial_filter_area)

    # make sure that new file is closed properly before reopening...
    ds_out = None

    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromEPSG(4326)

    ds_source = ogr.GetDriverByName('GPKG').Open(ofile, update=0)
    source_layer = ds_source.GetLayerByName(source_layer_name)

    path = os.path.join(str(self.currentSampleNumber()), 'wgs84', 'wgs84.gpkg')
    ds_dest = ogr.GetDriverByName('GPKG').Open(path, update=1)

    clip_layer = ds_dest.GetLayerByName(clip_layer_name)

    dest_layer = ds_dest.CreateLayer(dest_layer_name, geom_type=dest_layer_type, srs=spatial_ref)

    clip_layer = ds_dest.GetLayerByName(clip_layer_name)

    source_layer.Clip(clip_layer, dest_layer, options=['SKIP_FAILURES=YES'])

    dest_layer = None
    ds_source = None
    ds_dest = None






  def reproject_laea(self):

    source = os.path.join(str(self.currentSampleNumber()), 'wgs84', 'wgs84.gpkg')

    dest = os.path.join(str(self.currentSampleNumber()), 'laea', 'laea.gpkg')

    cmd = r'{} -q -s_srs EPSG:4326 -t_srs "+proj=laea +lon_0={} +lat_0={} +R=0 +x_0=0 +y_0=0 +units=m +no_defs" {} {}'.format(settings.path_ogr2ogr, self.longitude, self.latitude, dest, source)

    subprocess.check_call(cmd, shell=True)


  def get_extent(self, halo_size, cellsize):
    # calculates new extent based on the reprojected OMI cell, halo size and cellsize

    # Get envelope of reprojected OMI
    source = os.path.join(str(self.currentSampleNumber()), 'laea', 'laea.gpkg')

    layer_name = 'extent'

    ds_source = ogr.GetDriverByName('GPKG').Open(source, update=0)
    source_layer = ds_source.GetLayerByName(layer_name)

    source_features = source_layer.GetNextFeature()

    env = source_features.GetGeometryRef().GetEnvelope()

    omi_minX = env[0]
    omi_maxX = env[1]
    omi_minY = env[2]
    omi_maxY = env[3]

    halo = halo_size

    # Calculate new extent of the underlying raster

    # place origin in cell centre...
    minX = 0.0 - self.radius_x * cellsize
    while minX > omi_minX:
      minX -= cellsize
    minX -=  halo

    maxX = 0.0 + self.radius_x * cellsize
    while maxX < omi_maxX:
      maxX +=  cellsize
    maxX += halo

    minY = 0.0  - self.radius_y * cellsize
    while minY > omi_minY:
      minY -= cellsize
    minY -= halo

    maxY = 0.0  + self.radius_y * cellsize
    while maxY < omi_maxY:
      maxY += cellsize
    maxY += halo

    return minX, maxX, minY, maxY


  def create_clone(self, minX, maxX, minY, maxY, cellsize, filename):
    # Burn the extent of the OMI cell into a clone map

    source_layer_name = 'extent'
    source = os.path.join(str(self.currentSampleNumber()), 'laea', 'laea.gpkg')

    raster_filename = os.path.join(str(self.currentSampleNumber()), 'laea', filename)

    if os.path.exists(raster_filename):
      os.remove(raster_filename)

    ## to boolean somehow triggers a segfault with particulare cell sizes (25000 works, others not?)
    command = r'{} -at -q -burn 1 -of PCRaster -co "PCRASTER_VALUESCALE=VS_NOMINAL" -ot Int32 -tr {} {} -te {} {} {} {} -l {} {} {}'.format(settings.path_gdal_rasterize, cellsize, cellsize, minX, minY, maxX, maxY, source_layer_name, source, raster_filename)


    # Hack to make a Boolean clone map
    subprocess.check_call(command, shell=True)
    pcraster.setclone(raster_filename)
    raster = pcraster.readmap(raster_filename)
    pcraster.report(pcraster.boolean(raster), raster_filename)


  def create_landuse(self, minX, maxX, minY, maxY, cellsize):
    # Burn the industrial area into a raster map

    source_layer_name = 'industry'
    source = os.path.join(str(self.currentSampleNumber()), 'laea', 'laea.gpkg')

    raster_filename = os.path.join(str(self.currentSampleNumber()), 'laea', 'halo_industry.map')

    if os.path.exists(raster_filename):
      os.remove(raster_filename)

    ## to boolean somehow triggers a segfault with particulare cell sizes (25000 works, others not?)
    command = r'{} -at -q -burn 1 -of PCRaster -co "PCRASTER_VALUESCALE=VS_NOMINAL" -ot Int32 -tr {} {} -te {} {} {} {} -l {} {} {}'.format(settings.path_gdal_rasterize, cellsize, cellsize, minX, minY, maxX, maxY, source_layer_name, source, raster_filename)

    subprocess.check_call(command, shell=True)

    # Assign cell area
    pcraster.setclone(raster_filename)
    raster = pcraster.scalar(pcraster.readmap(raster_filename)) * pcraster.cellarea()
    pcraster.report(raster, raster_filename)


  def calc_buffer(self, ofilename):

    source_def = '"+proj=laea +lon_0={} +lat_0={} +R=0 +x_0=0 +y_0=0 +units=m +no_defs"'.format(self.longitude, self.latitude)
    proj_dir = os.getcwd()

    w_dir = os.path.join(str(self.currentSampleNumber()), 'laea')

    os.chdir(w_dir)

    script_file = os.path.join(proj_dir, 'make_buffer.py')
    for buffer_size in self.buffer_sizes:

      start_b = datetime.datetime.now()
      nr_cpus = settings.buffer_cpus
      cmd = '{} {} halo_clone.map halo_{}.map {} {}'.format(settings.path_python_exe, script_file, ofilename, buffer_size, nr_cpus)
      subprocess.check_call(cmd, shell=True)

      # cmd = '{} --nothing --clone clone.map halo_{}_{}.map {}_{}.map'.format(settings.path_resample, ofilename, buffer_size, ofilename, buffer_size)
      # subprocess.check_call(cmd, shell=True)

      # cmd = '{} -q -overwrite -cutline laea.gpkg -cl extent -crop_to_cutline -s_srs {} halo_{}_{}.map {}_{}.tiff'.format(settings.path_gdalwarp, source_def, ofilename, buffer_size, ofilename, buffer_size)

      cmd = '{} -q -overwrite -tr {} {} -te {} {} {} {} -s_srs {} halo_{}_{}.map {}_{}.tiff'.format(settings.path_gdalwarp, self.cellsize, self.cellsize, self.minX, self.minY, self.maxX, self.maxY, source_def, ofilename, buffer_size, ofilename, buffer_size)
      subprocess.check_call(cmd, shell=True)

      cmd = '{} -q {}_{}.tiff {}_{}.map'.format(settings.path_gdal_translate, ofilename, buffer_size, ofilename, buffer_size)
      subprocess.check_call(cmd, shell=True)

      # remove temporary file
      os.remove('{}_{}.tiff'.format(ofilename, buffer_size))


    os.chdir(proj_dir)





  def remove_halo_maps(self):

    proj_dir = os.getcwd()

    w_dir = os.path.join(str(self.currentSampleNumber()), 'laea')

    os.chdir(w_dir)


    os.remove('halo_clone.map')
    os.remove('halo_industry.map')

    for buffer_size in self.buffer_sizes:


      os.remove('halo_industry_{}.map'.format(buffer_size))

      for road_class in self.road_classes:

        os.remove('halo_road_class_{}_{}.map'.format(road_class, buffer_size))


    for road_class in self.road_classes:
      os.remove('halo_road_class_{}.map'.format(road_class))
      os.remove('tmp_roads_{}.map'.format(road_class))

    os.chdir(proj_dir)



  def create_road_rasters(self, road_class, minX, maxX, minY, maxY, cellsize):

    source_layer_name = 'road_class_{}'.format(road_class)
    source = os.path.join(str(self.currentSampleNumber()), 'laea', 'laea.gpkg')

    raster_file = os.path.join(str(self.currentSampleNumber()), 'laea', 'tmp_roads_{}.map'.format(road_class))


    ## to boolean somehow triggers a segfault
    cmd = r'{} -q -at -burn 1 -of PCRaster -co "PCRASTER_VALUESCALE=VS_NOMINAL" -ot Int32 -tr {} {} -te  {} {} {} {} -l {} {} {} '.format(settings.path_gdal_rasterize, cellsize, cellsize, minX, minY, maxX, maxY, source_layer_name, source, raster_file)

    subprocess.check_call(cmd, shell=True)
    # we don't need the generated xml file
    xml_filename = '{}.aux.xml'.format(raster_file)
    os.remove(xml_filename)


    pcraster.setclone(raster_file)
    raster = pcraster.readmap(raster_file)
    pcraster.report(pcraster.ifthen(pcraster.boolean(raster), pcraster.boolean(1)), raster_file)

    ifile = os.path.join(str(self.currentSampleNumber()), 'laea',  'tmp_roads_{}.map'.format(road_class))
    ofile = os.path.join(str(self.currentSampleNumber()), 'laea',  'tmp_roads_{}.csv'.format(road_class))
    cmd = '{} --nothing -s , -f "15.6f" {} {}'.format(settings.path_map2col ,ifile, ofile)
    subprocess.check_call(cmd, shell=True)


  def create_fishgrid(self, road_class, cellsize):
    # We limit the amount of features required to calculate the road lengths
    # by just making clip features at road cell positions

    path = os.path.join(str(self.currentSampleNumber()), 'laea', 'laea.gpkg')

    ds = ogr.GetDriverByName('GPKG').Open(path, update=1)
    tmp_layer = ds.GetLayerByName('extent')

    spatial_ref = tmp_layer.GetSpatialRef()

    layername = 'fish_{}'.format(road_class)

    if ds.GetLayerByName(layername):
      ds.DeleteLayer(layername)
    outLayer = ds.CreateLayer(layername, geom_type=ogr.wkbPolygon, srs=spatial_ref)

    featureDefn = outLayer.GetLayerDefn()
    outLayer.StartTransaction()

    dist = cellsize / 2.0

    csv_filename = os.path.join(str(self.currentSampleNumber()), 'laea', 'tmp_roads_{}.csv'.format(road_class))
    with open(csv_filename, "r") as csv_file:
      reader = csv.reader(csv_file, delimiter=',')
      for row in reader:
          pointX = float(row[0])
          pointY = float(row[1])

          ring = ogr.Geometry(ogr.wkbLinearRing)
          ring.AddPoint(pointX - dist, pointY + dist)
          ring.AddPoint(pointX + dist, pointY + dist)
          ring.AddPoint(pointX + dist, pointY - dist)
          ring.AddPoint(pointX - dist, pointY - dist)

          ring.AddPoint(pointX - dist, pointY + dist)

          poly = ogr.Geometry(ogr.wkbPolygon)
          poly.AddGeometry(ring)

          outFeature = ogr.Feature(featureDefn)
          outFeature.SetGeometry(poly)
          outLayer.CreateFeature(outFeature)
          outFeature = None

    outLayer.CommitTransaction()


  def intersect_roads(self, road_class):
    # Calculate road length per raster cell

    path = os.path.join(str(self.currentSampleNumber()), 'laea', 'laea.gpkg')

    ds = ogr.GetDriverByName('GPKG').Open(path, update=1)
    tmp_layer = ds.GetLayerByName('extent')

    spatial_ref = tmp_layer.GetSpatialRef()

    fish_layername = 'fish_{}'.format(road_class)
    road_layername = 'road_class_{}'.format(road_class)
    intersect_layername = 'intersect_{}'.format(road_class)

    road_layer = ds.GetLayerByName(road_layername)
    fish_layer = ds.GetLayerByName(fish_layername)

    if ds.GetLayerByName(intersect_layername):
      ds.DeleteLayer(intersect_layername)

    intersect_layer = ds.CreateLayer(intersect_layername, geom_type=ogr.wkbLineString, srs=spatial_ref)

    roadlenField = ogr.FieldDefn("roadlen", ogr.OFTReal)
    intersect_layer.CreateField(roadlenField)


    intersect_layer.StartTransaction()
    road_layer.Intersection(fish_layer, intersect_layer)

    # length for each feature
    csvname = os.path.join(str(self.currentSampleNumber()), 'laea','{}.csv'.format(road_layername))
    tot_val = 0.0


    with open(csvname, 'w') as content:
      for feature in intersect_layer:
        geom = feature.GetGeometryRef()
        val = geom.Length()

        feature.SetField("roadlen", val)
        intersect_layer.SetFeature(feature)


        x = feature.GetGeometryRef().Centroid().GetX()
        y = feature.GetGeometryRef().Centroid().GetY()

        row = '{},{},{}\n'.format(x,y,val)
        content.write(row)

        tot_val += val

    intersect_layer.CommitTransaction()

    # Create PCRaster map
    clone_path = os.path.join(str(self.currentSampleNumber()), 'laea','halo_clone.map')

    out_path = os.path.join(str(self.currentSampleNumber()), 'laea', 'halo_{}.map'.format(road_layername))

    pcraster.setclone(clone_path)

    if tot_val > 0.0:
      cmd = '{} --nothing --clone {} -t -S -x 1 -y 2 -v 3 {} {}'.format(settings.path_col2map, clone_path, csvname, out_path)
      subprocess.check_call(cmd, shell=True)

      # Replace missing values
      raster = pcraster.cover(out_path, 0.0)
    else:
      # No roads of particular type in the area
      raster = pcraster.scalar(0.0)

    pcraster.report(raster, out_path)



  def test_to_run(self):
    dest_dir = os.path.join(self.result_dir, str(self.area_id))

    if os.path.exists(dest_dir):
      return False

    return True


  def finalise(self, files):
    # Copy required results to output directory
    dest_dir = os.path.join(self.result_dir, str(self.area_id))

    assert not os.path.exists(dest_dir), 'Output directory "{}" exists'.format(dest_dir)

    os.mkdir(dest_dir)

    dest_dir_wgs = os.path.join(dest_dir, 'wgs84')
    dest_dir_laea = os.path.join(dest_dir, 'laea')
    os.mkdir(dest_dir_wgs)
    os.mkdir(dest_dir_laea)

    source_dir_wgs = os.path.join(str(self.currentSampleNumber()), 'wgs84')
    source_dir_laea = os.path.join(str(self.currentSampleNumber()), 'laea')



    #LAEA
    shutil.move(os.path.join(source_dir_laea, 'laea.gpkg'), dest_dir_laea)
    shutil.move(os.path.join(source_dir_laea, 'clone.map'), dest_dir_laea)
    shutil.move(os.path.join(source_dir_laea, 'clone.map.aux.xml'), dest_dir_laea)
    # shutil.move(os.path.join(source_dir_laea, 'halo_clone.map'), dest_dir_laea)
    # shutil.move(os.path.join(source_dir_laea, 'halo_clone.map.aux.xml'), dest_dir_laea)

    for buffer_size in self.buffer_sizes:
      fname1 = os.path.join(source_dir_laea, 'industry_{}.map'.format(buffer_size))
      fname2 = os.path.join(source_dir_laea, 'industry_{}.map.aux.xml'.format(buffer_size))
      shutil.move(fname1, dest_dir_laea)
      shutil.move(fname2, dest_dir_laea)

    for road_class in self.road_classes:
      for buffer_size in self.buffer_sizes:
        fname1 = os.path.join(source_dir_laea, 'road_class_{}_{}.map'.format(road_class, buffer_size))
        fname2 = os.path.join(source_dir_laea, 'road_class_{}_{}.map.aux.xml'.format(road_class, buffer_size))
        shutil.move(fname1, dest_dir_laea)
        shutil.move(fname2, dest_dir_laea)

    # WGS84
    shutil.move(os.path.join(source_dir_wgs, 'wgs84.gpkg'), dest_dir_wgs)


    for f in files:
      fname1 = os.path.join(source_dir_laea, '{}.map'.format(f))
      fname2 = os.path.join(source_dir_laea, '{}.map.aux.xml'.format(f))
      shutil.move(fname1, dest_dir_laea)
      shutil.move(fname2, dest_dir_laea)



  def convert_raster(self, filename):

    wgs_dir = os.path.join(str(self.currentSampleNumber()), 'wgs84')
    laea_dir = os.path.join(str(self.currentSampleNumber()), 'laea')

    input_file = os.path.join(settings.data_sources, filename)
    output_file = os.path.join(laea_dir, 'tmp_{}'.format(filename))

    # Cut in wgs and rewarp to laea
    cmd = r'{} -q -s_srs EPSG:4326 -t_srs "+proj=laea +lon_0={} +lat_0={} +R=0 +x_0=0 +y_0=0 +units=m +no_defs" -cutline {} -cl halo -crop_to_cutline  {}.tiff {}.tiff'.format(settings.path_gdalwarp, self.longitude, self.latitude, os.path.join(wgs_dir, 'wgs84.gpkg'), input_file, output_file)
    subprocess.check_call(cmd, shell=True)


    # Clip to area of interest
    input_file = output_file
    output_file = os.path.join(laea_dir, 'tmp_{}_crop'.format(filename))
    cmd = r'{} -q -tr {} {} -projwin {} {} {} {} -r cubic {}.tiff {}.tiff'.format(settings.path_gdal_translate, self.cellsize, self.cellsize, self.minX, self.maxY, self.maxX, self.minY, input_file, output_file)
    subprocess.check_call(cmd, shell=True)


    # To PCRaster
    input_file = output_file
    output_file = os.path.join(laea_dir,filename)
    cmd = '{} -q {}.tiff {}.map'.format(settings.path_gdal_translate, input_file, output_file)
    subprocess.check_call(cmd, shell=True)






  def initial(self):
    start = datetime.datetime.now()

    try:
      cols = self.omi_centres[1] #omi_centres.shape[1]
      self.longitude = self.omi_centres[self.currentSampleNumber() - 1][0]
      self.latitude = self.omi_centres[self.currentSampleNumber() - 1][1]
      self.area_id = int(self.omi_centres[self.currentSampleNumber() - 1][2])
    except IndexError as err:
      self.longitude = self.omi_centres[0]
      self.latitude = self.omi_centres[1]
      self.area_id = int(self.omi_centres[2])

    # Calculate only if current area was not done yet
    if self.test_to_run() == False:
      return

    self.make_directories()


    # Cell centre/projection centre
    self.make_wgs84_point()

    # Cell extent from cell centre (clone map)
    self.make_wgs84_box('extent', self.radius_x, self.radius_y)


    # OMI cell + halo
    # size of the halo is a bit a guess but should be large enough
    # such that the reprojected map also has a sufficient halo
    halo_x = self.radius_x + self.halo_x
    halo_y = self.radius_y + self.halo_y
    self.make_wgs84_box('halo', halo_x, halo_y)


    # use the halo layer to clip input data (roads/landuse/...)
    clip_layer = 'halo'
    dest_layer = 'industry'
    self.clip_wgs(self.industry_source, 'multipolygons', clip_layer, dest_layer, ogr.wkbPolygon)

    for road_class in self.road_classes:
      source = os.path.join(self.road_sources, 'gap_class_{}.gpkg'.format(road_class))
      dest_layer = 'road_class_{}'.format(road_class)
      self.clip_wgs(source, 'lines', clip_layer, dest_layer, ogr.wkbLineString)


    # Reproject all the input data sources to a local LAEA
    self.reproject_laea()

    # Obtain extent for the LAEA areas, add halo in metres
    minX, maxX, minY, maxY = self.get_extent(self.halo_size, self.cellsize)

    # Extent of the area of interest
    # hm, refactor....
    self.minX, self.maxX, self.minY, self.maxY = minX + self.halo_size, maxX - self.halo_size, minY + self.halo_size, maxY - self.halo_size


    # Make PCRaster maps of the datasets
    # Create clone maps, with and without halo. without used for the cropping
    self.create_clone(minX, maxX, minY, maxY, cellsize, 'halo_clone.map')
    # self.create_clone(minX + self.halo_size, maxX - self.halo_size, minY + self.halo_size, maxY - self.halo_size, cellsize, 'clone.map')
    self.create_clone(self.minX, self.maxX, self.minY, self.maxY, self.cellsize, 'clone.map')

    # Land use industial
    self.create_landuse(minX, maxX, minY, maxY, cellsize)

    # Roads require a few more steps
    for road_class in self.road_classes:
      self.create_road_rasters(road_class, self.minX, self.maxX, self.minY, self.maxY, cellsize)
      self.create_fishgrid(road_class, cellsize)
      self.intersect_roads(road_class)


    # Calculate buffers
    self.calc_buffer('industry')
    for road_class in self.road_classes:
      fname = 'road_class_{}'.format(road_class)
      self.calc_buffer(fname)

    files  = ['elevation', 'pop1k', 'pop3k', 'pop5k', 'temperature_2m_10', 'temperature_2m_11', 'temperature_2m_12', 'temperature_2m_1', 'temperature_2m_2', 'temperature_2m_3', 'temperature_2m_4', 'temperature_2m_5', 'temperature_2m_6', 'temperature_2m_7', 'temperature_2m_8', 'temperature_2m_9', 'wind_speed_10m_10', 'wind_speed_10m_11', 'wind_speed_10m_12', 'wind_speed_10m_1', 'wind_speed_10m_2', 'wind_speed_10m_3', 'wind_speed_10m_4', 'wind_speed_10m_5', 'wind_speed_10m_6', 'wind_speed_10m_7', 'wind_speed_10m_8', 'wind_speed_10m_9', 'Rsp', 'OMI_mean_filt', 'trop_mean_filt']



    # this also moves to output directory, keep it after finalise as that creates the result folder...
    for f in files:
      self.convert_raster(f)


    # Copy results to corresponding result directory
    self.finalise(files)

    # We clean working dir due to storage capacity...
    shutil.rmtree(os.path.join(os.getcwd(), str(self.currentSampleNumber())))



    end = datetime.datetime.now()
    print('        task {:5d} long {:8.2f} lat {:8.2f} id {:12d} {}'.format(self.currentSampleNumber(), self.longitude, self.latitude, self.area_id, end - start))
    sys.stdout.flush()


# Cells to process
centres = numpy.loadtxt(settings.coord_centre, delimiter=',')

nr_samples = None

try:
  cols = centres.shape[1]
  nr_samples = centres.shape[0]
except IndexError as err:
  nr_samples = 1

industry_source = settings.industry_source

road_sources = settings.road_sources

road_classes = settings.road_classes

buffersizes = settings.road_buffersizes


# Target cell size
cellsize = settings.cellsize # in m, can put higher value for testing
radius_x = settings.radius_x # degree, half side of the square
radius_y = settings.radius_y
halo_x = settings.halo_x # 5km for the boarder
halo_y = halo_x

result_dir = settings.result_dir

# Halo should match the largest buffer, plus a small safety margin
halo_size = buffersizes[-1] + cellsize

myModel = CalcPredictor(cellsize, buffersizes, halo_size, industry_source, road_sources, road_classes, radius_x, radius_y, halo_x, halo_y, result_dir)
staticModel = StaticFramework(myModel)
mcModel = MonteCarloFramework(staticModel, nrSamples=nr_samples)
mcModel.setQuiet(True)

#mcModel.setForkSamples(True, 48)

s = datetime.datetime.now()
mcModel.run()
e = datetime.datetime.now()
print('start: {} end: {} runtime: {}'.format(s, e, e - s))
sys.stdout.flush()


