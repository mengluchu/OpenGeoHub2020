import os
import sys
import numpy
import multiprocessing
import ctypes
import argparse

import pcraster as pcr


# the result map shared between the threads
shared = None


def output_filename(filename, buffer_size):
  head, tail = os.path.split(filename)
  tmp = tail.split(".")
  fname = "{0}_{1}.map".format(tmp[0], buffer_size * int(pcr.celllength()))
  return fname


def calc_buffer_size(radius_metres):
  return radius_metres / int(pcr.celllength())


def make_shared(rows, cols):
  shared_base = multiprocessing.Array(ctypes.c_float, rows * cols)
  shared = numpy.ctypeslib.as_array(shared_base.get_obj())
  shared = shared.reshape(rows, cols)
  shared.fill(0.0)
  return shared


def conv_concurrent(row, def_param=shared):

  y,x = numpy.ogrid[-buffer_size : buffer_size + 1, -buffer_size : buffer_size + 1]
  mask = x*x + y*y <= buffer_size * buffer_size

  # hack, correct for missing halo...
  xmin = int(buffer_size + 1)
  xmax = int(cols - buffer_size - 1)

  for c in range(xmin, xmax):
    cell_value = pcr.cellvalue(map_defined, row + 1, c + 1)
    if cell_value[1] == True and cell_value[0] == True:
      a = map_scalar[row - buffer_size:row + buffer_size + 1, c - buffer_size: c + buffer_size + 1]
      tmp = a[mask]

      value = numpy.sum(tmp)
      shared[row][c] = value




if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description="Script to calculate the buffers")
  parser.add_argument("locations", type=str, help="map with locations to calculate")
  parser.add_argument("source", type=str, help="map with predictor variable value")
  parser.add_argument("buffer", type=int, help="bufer size in metres")
  parser.add_argument("cores", type=int, help="number of cores to use")
  args = parser.parse_args()

  locations_to_calculate = args.locations
  map_to_process = args.source
  map_defined = pcr.readmap(locations_to_calculate)
  buffer_size = int(calc_buffer_size(args.buffer))
  nr_cores = args.cores
  output_name = output_filename(map_to_process, buffer_size)

  rows = pcr.clone().nrRows()
  cols = pcr.clone().nrCols()

  shared = make_shared(rows, cols)
  map_scalar = pcr.pcr2numpy(pcr.readmap(map_to_process), 0)

  # hack, correct for missing halo...
  ymin = buffer_size + 1
  ymax = rows - buffer_size - 1

  pool = multiprocessing.Pool(nr_cores)

  pool.map(conv_concurrent, range(int(ymin), int(ymax)), 1)

  res = pcr.numpy2pcr(pcr.Scalar, shared, -1)
  shared = None
  res = pcr.ifthen(map_defined==1, res)
  pcr.report(res, output_name)
  sys.exit(0)
