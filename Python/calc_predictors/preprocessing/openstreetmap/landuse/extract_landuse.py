import subprocess


osmium = 'osmium'

fname = '/data/openstreetmap/osm_data/planet-190107'




def extract(keyword, value, out_fname):

  cmd = "{0} tags-filter {1}.osm.pbf nwr/{2}={3} -o gap_{4}.osm.pbf".format(osmium, fname, keyword, value, out_fname)

  print(cmd)
  subprocess.check_call(cmd, shell=True)

  cmd = "ogr2ogr -f GPKG gap_{}.gpkg gap_{}.osm.pbf".format(out_fname, out_fname)
  print(cmd)
  subprocess.check_call(cmd, shell=True)

landuses = [
  #"commercial",
  "industrial",
  #"residential",
  #"retail",
  #"port",
  #"forest",
  #"farmland",
  #"quarry",
  #"railway"
  ]

for r in landuses:
  extract("landuse", r, '{}'.format(r))
