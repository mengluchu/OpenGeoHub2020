import shutil
import os




for d in range(1, 2500):
  path = '{}'.format(d)
  if os.path.exists(path):
    shutil.rmtree(path)
