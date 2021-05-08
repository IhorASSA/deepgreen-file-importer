#!/usr/bin/python
# -*- coding: utf-8 -*-
"""DeepGreen-DEMO-ver2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Jdn5fJaX8bfYvtfqhhoY89ETsFp7Rtfp

### Installation Project Libraries
"""

# !pip install SQLAlchemy GeoAlchemy2 geopandas PyDrive psycopg2 --upgrade
# !pip install geopandas oauth2client --upgrade

"""## Import Project Libraries

---


"""

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


logger.basicConfig(
    filename="log_file_test.log",
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logger.DEBUG
)

logger.info("This is a test log ..")

"""## Constants and functions

### Define Constants
"""

EPSG = 3857
URL = 'https://lk.ukrforest.com/map/get-point-info?point=[{},{}]'

JSON_RESPONSE = {
    'index': '',
    'region': '',
    'district': '',
    'quarter': '',
    'square': '',
    'cutting_ticket_url': '',
    'cutting_status': '',
    'cutting_volume_approved': '',
    'cutting_user': '',
    'cutting_method': '',
    'coords': {
        'centroid': [],
        # 'polygon': []
    },
    'raw_response': {},
    'url': None
}

COMMA_LIST = ', , ,'
STRONG_LIST = '<strong> <strong> <strong> <strong>' # 4.times('<strong> ').join() - так не можна Саша? :)
CUT_STATUS = 'Рубка'
CUT_STATUS_STARTED = 'Рубка - Розпочата'
CUT_STATUS_CLOSED = 'Рубка - Закрита'
CUT_STATUS_NOT_STARTED = 'Рубка - Не розпочата'
COL_START = ['datetime', 'ID', 'CODE', 'CODE_TEXT', 'area', 'Extend', 'geometry']
COL_INFO = ['region', 'district', 'quarter', 'square',
            'cutting_ticket_url', 'cutting_status', 'cutting_volume_approved',
            'cutting_user', 'cutting_method']
COL_END = ['url', 'coords',	'raw_response']

"""### Code Functions & Routines

### System Functions
"""

def setup_drive():
  # 1. Authenticate and create the PyDrive client.
  auth.authenticate_user()
  gauth = GoogleAuth()
  gauth.credentials = GoogleCredentials.get_application_default()
  return GoogleDrive(gauth)



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

def custom_draw(x):
  if x['properties']['CODE'] == 1:
    return {'fillColor': '#00ff00', 'fillOpacity': 0.5, 'weight': 2}
  elif x['properties']['CODE'] == 2:
    return {'fillColor': '#ff0000', 'fillOpacity': 0.5, 'weight': 2}
  elif x['properties']['CODE'] == 3:
    return {'fillColor': '#ff69b4', 'fillOpacity': 0.5, 'weight': 2}
  elif x['properties']['CODE'] == 4:
    return {'fillColor': '#0000ff', 'fillOpacity': 0.5, 'weight': 1}
  else:
    return {'fillColor': '#c0c0c0', 'fillOpacity': 0.5, 'weight': 1}

def save_to_postgres(gdf, table_name):
  engine = create_engine(
     # "postgresql://deepgreen:HJKj4oiIUs-8@ec2-52-204-66-46.compute-1.amazonaws.com:5432/deepgreen"
     "postgresql://deepgreen:deepgreen2021MT!@ec2-15-188-127-126.eu-west-3.compute.amazonaws.com:5432/deepgreen"
    # "postgresql://deepgreen:deepgreen2021MT!@localhost:5432/deepgreen"
  )
  gdf.to_postgis(name=table_name, con=engine, if_exists='append', index=True)

def get_datetime_from_file(file_for_processing):
  with open(file_for_processing, 'rb') as fd:
    json_file = json.load(fd)

  # raise without excuse :) if any
  return pd.to_datetime(json_file.get('name', '').replace('_', '-'))

"""### Parsing API response and enriching data

#### Parsing and rules identification utils
"""

def parse_response(response, result):
  static_info = [item.strip() for item in COMMA_LIST.split(',')]
  cutting_info = [item.strip() for item in STRONG_LIST.split('<strong>')]
  try:
      response_data = response.get('data', [{}])
      if response_data:
          _static_info = response_data[0].get('static', COMMA_LIST).split(',')
          if _static_info != COMMA_LIST: # and len(_static_info) == len(static_info):
              static_info = [item.strip() for item in _static_info]

          _cutting_info = response_data[0].get('cutting', STRONG_LIST).split('<strong>')
          if _cutting_info != STRONG_LIST: # and len(_cutting_info) == len(cutting_info):
              _cutting_info = [item.replace('</br>', '').replace('<br>', '').replace('</strong>', '').strip() for item in _cutting_info]
              while len(_cutting_info) != len(cutting_info):
                _cutting_info.append('')
              cutting_info = _cutting_info
              # if cutting_info[1] != '' and cutting_info[1].find('Закрита') == -1:
              #     print(cutting_info)
  except Exception as err:
      print('Response={} | Error={}'.format(response, err))

  result['region'] = static_info[0].strip()
  result['district'] = static_info[1].strip()
  result['quarter'] = static_info[2].strip()
  result['square'] = static_info[3].strip()

  result['cutting_ticket_url'] = cutting_info[0].strip()
  result['cutting_status'] = cutting_info[1].strip()
  result['cutting_volume_approved'] = cutting_info[2].strip()
  result['cutting_user'] = cutting_info[3].strip()
  result['cutting_method'] = cutting_info[4].strip()

  return result

def set_rules_ver02(result):
  """
    Rules prepared for DEMO-1 by Sash
  """
  if result['region'] != '':
    if CUT_STATUS_STARTED in result['cutting_status']:       # Legal
      result['CODE'] = 1
      result['CODE_TEXT'] = 'Легальна'
    elif CUT_STATUS_CLOSED in result['cutting_status']:      # Not Legal
      result['CODE'] = 2
      result['CODE_TEXT'] = 'Не легальна (Рубка - Закрита)'
    elif CUT_STATUS_NOT_STARTED in result['cutting_status']: # Not Legal | Don't started
      result['CODE'] = 3
      result['CODE_TEXT'] = 'Не легальна (Рубка - Не розпочата)'
    else:
      result['CODE'] = 5                                     # Unknown case
      result['CODE_TEXT'] = 'Невідомий сценарій'
  else:
    result['CODE'] = 4                                     # User is not identified
    result['CODE_TEXT'] = 'Не ідентифікований лісокористувач'

  return result

def set_rules_ver03(result):
  """
    Rules prepared for DEMO-2 by Client&Team
  """
  if result['region'] != '':
    if CUT_STATUS_STARTED in result['cutting_status']:       # Legal
      result['CODE'] = 1
      result['CODE_TEXT'] = 'Легальна діюча'
    elif CUT_STATUS_CLOSED in result['cutting_status']:      # Legal "Closed"
      result['CODE'] = 2
      result['CODE_TEXT'] = 'Легальна закрита'
    elif CUT_STATUS_NOT_STARTED in result['cutting_status']: # Legal "Don't started"
      result['CODE'] = 3
      result['CODE_TEXT'] = 'Легальна не розпочата'
    elif CUT_STATUS in result['cutting_status']:
      result['CODE'] = 6                                     # Unknown case - "Rubka Karl", simply 'Rubka'
      result['CODE_TEXT'] = 'Рубка'
    else:
      result['CODE'] = 4                                     # Not Legal
      result['CODE_TEXT'] = 'Нелегальна відсутній лісорубний'
  else:
    result['CODE'] = 5                                       # Place is not identified
    result['CODE_TEXT'] = 'Проблеми ідентифікації місцерозташування'

  return result

"""#### Main Parsing and Enrichment Flow"""

def send_requests(polygon_flatten, rules_strategy='ver03'):
    result_list = []
    idx = 1
    for idx, point in set(polygon_flatten):
        result = JSON_RESPONSE.copy()
        try:
            result['index'] = idx
            result.setdefault('coords', {})['centroid'] = point
            # result.setdefault('coords', {})['polygon'] = polygon_flatten
            url = URL.format(point[0], point[1])
            result['url'] = url

            response = requests.get(url).json()

            result['raw_response'] = response
            # Defaults
            result = parse_response(response, result)
            # Set the rules
            if rules_strategy.lower() == 'ver02':
              result = set_rules_ver02(result)
            else:
              result = set_rules_ver03(result)
        except Exception as err:
            result.setdefault('raw_response', err)
            print('ERROR', url, result, err)
        idx += 1
        result_list.append(result)
    print('Parsing is finished. Total requests in this session: {}'.format(len(result_list)))
    return pd.DataFrame(result_list).set_index(keys='index')

"""### Main multi-processing crawling flow"""

def iterate_over_centroids(gdf, epsg=3857, limit=5, chunk_size=7):
    num_cpus = psutil.cpu_count(logical=False)

    #print(gdf.crs)
    process_pool = Pool(processes=num_cpus*2)
    start = time.time()

    gdf_new = gdf.to_crs(epsg=epsg)
    print(gdf_new.crs)

    # Start processes in the pool and concat dataframes to one dataframe
    dfs = process_pool.map(
        send_requests,
        [item for item in make_centroid_sub_lists(gdf_new.head(limit), chunk_size)]
      )

    df_processed = pd.concat(
        dfs,
        axis='rows',
        ignore_index=False
    )
    gdf_merged = pd.concat(
        [
            gdf_new.head(limit),
            df_processed
        ],
        axis='columns',
        ignore_index=False
    )

    gdf_merged = gdf_merged.reindex(list(COL_START + COL_INFO + COL_END), axis=1)

    gdf_merged.loc[:, 'CODE'] = gdf_merged.CODE.fillna(5)
    gdf_merged.loc[:, 'CODE'] = gdf_merged.CODE.astype(int)

    gdf_merged.columns = [col.lower() for col in gdf_merged.columns]
    print('Completed in: {} sec(s)'.format(time.time() - start))

    return gdf_merged

"""## Main Flow Execution

---
"""
# file_for_processing = sys.argv[1]
file_for_processing = "/home/archer/dev/deepgreen-camel-clj/target/2020_09_03.geojson"


total_requests_to_process = -1

gdf = gpd.read_file(file_for_processing).to_crs(3857).tail(total_requests_to_process)
file_datetime = get_datetime_from_file(file_for_processing)
gdf.loc[:, 'datetime'] = file_datetime

gdf = pd.concat(
    [
      gdf
    ],
    axis='rows',
    ignore_index=True
)
# Normalize the index
gdf.index = pd.Index([i for i in range(1, gdf.shape[0] + 1)])

gdf.head(5)

gdf.datetime.unique()

"""### 3. Start crawling and parsing"""

gdf_enriched = iterate_over_centroids(
    gdf,
    epsg=3857,
    limit=total_requests_to_process,
    chunk_size=50
)

gdf_enriched.info()

gdf_enriched.code.unique()

gdf_enriched[gdf_enriched.code == 3].head(3)

gdf_enriched[['code']].groupby(by='code').size().reset_index(name='counts')

# gdf_enriched.loc[:, 'coords'] = gdf_enriched.coords.apply(lambda x: x.get('centroid'))
# [MultiPolygon([feature]) if type(feature) == Polygon     else feature
# gdf_enriched.loc[:, 'geometry'] = [MultiPolygon(list(x)) for x in gdf_enriched.coords]
from shapely import wkt

gdf_enriched_centroid = gdf_enriched[['code']].copy()
gdf_enriched_centroid.loc[:, 'geometry'] = gdf_enriched.centroid.copy()
gdf_enriched_centroid = gpd.GeoDataFrame(gdf_enriched_centroid, geometry='geometry')
gdf_enriched_centroid.head(3)

"""### 4. Save enriched data to PostgreSQL DB



"""

# TABLE_NAME='pg_deepgreen_demo_arsen'
TABLE_NAME='spatial_data'
save_to_postgres(gdf_enriched, table_name=TABLE_NAME)
print('Data is saved. Please review the table [{}]'.format(TABLE_NAME))

