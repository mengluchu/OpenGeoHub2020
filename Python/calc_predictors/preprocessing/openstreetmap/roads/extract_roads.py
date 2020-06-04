import subprocess




osmium = '/scratch/applications/bin/osmium'

fname = '/scratch/openstreetmap/osm_data/planet-190107'




def extract(keyword, value, out_fname):

  cmd = "{0} tags-filter {1}.osm.pbf nwr/{2}={3} -o gap_{4}.osm.pbf".format(osmium, fname, keyword, value, out_fname)

  print(cmd)
  subprocess.check_call(cmd, shell=True)

  cmd = "ogr2ogr -f GPKG gap_{}.gpkg gap_{}.osm.pbf".format(out_fname, out_fname)
  print(cmd)
  subprocess.check_call(cmd, shell=True)

  print('')


roads = [
  "motorway,motorway_link,trunk,trunk_link",
  "primary,primary_link",
  "secondary,secondary_link",
  "tertiary,tertiary_link",
  "residential,residential_link"
  ]


for i, r in enumerate(roads):
  extract('highway', r, 'class_{}'.format(i + 1))

