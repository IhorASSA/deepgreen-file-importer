import geopandas as gpd
import json
import logging as logger
import os
import numpy as np
import pandas as pd
import psutil
import requests
import time
import sys

from geopandas import GeoSeries
from itertools import islice
from multiprocessing import Pool
from shapely.geometry import Polygon, Point, MultiPolygon
from sqlalchemy import create_engine
from deepgreen_const import * 


def get_datetime_from_file(file_for_processing):
  with open(file_for_processing, 'rb') as fd:
    json_file = json.load(fd)

  # raise without excuse :) if any
  return pd.to_datetime(json_file.get('name', '').replace('_', '-').replace('lviv-', ''))


def make_sub_lists(list_in, chunk_size):
    list_in = iter(list_in)
    return iter(lambda: tuple(islice(list_in, chunk_size)), ())


def make_centroid_sub_lists(gdf, chunk_size):
    centroids = list(
        zip(
            gdf.index,
            zip(
                gdf.centroid.x.values,
                gdf.centroid.y.values)
        )
    )
    return make_sub_lists(centroids, chunk_size)


def save_to_postgres(gdf, table_name):
  engine = create_engine(PG_DB_CONNECTION_STRING)
  try:
    engine.execute('create extension postgis')
  except:
    pass
  gdf.to_postgis(name=table_name, con=engine, if_exists='append', index=True)
