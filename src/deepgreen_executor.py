#!/usr/bin/python
# -*- coding: utf-8 -*-

from deepgreen_parser import *
from deepgreen_rules import *
from deepgreen_utils import *


def send_requests(polygon_flatten, rules_strategy='ver03'):
    result_list = []
    for idx, point in set(polygon_flatten):
        result = JSON_RESPONSE.copy()  # Defaults
        result['index'], result['centroid'] = idx, point
        result['url'] = URL.format(point[0], point[1])
        try:
            result['raw_response'] = requests.get(result['url'])
            result['raw_response'] = result['raw_response'].json()
            result = parse_response(result['raw_response'], result)
            # Set the rules
            if result.get('CODE', 0) not in [CODE_INT_API_ERROR, CODE_INT_PARSER_ERROR]:
                if rules_strategy.lower() == 'ver02':
                    result = set_rules_ver02(result)
                else:
                    result = set_rules_ver03(result)
        except Exception as err:
            print('ERROR', result['url'], result['raw_response'], result, err)
            result['error_msg'] = '{}: {}'.format(result['raw_response'], err)
            result['CODE'] = CODE_INT_API_ERROR
            result['CODE_TEXT'] = CODE_TEXT_API_ERROR


        result_list.append(result)
    print('Parsing is finished. Total requests in this session: {}'.format(len(result_list)))
    return pd.DataFrame(result_list).set_index(keys='index')


def execute_enrichment(gdf, epsg=EPSG, limit=5, chunk_size=7):
    start = time.time()
    num_cpus = psutil.cpu_count(logical=False)
    process_pool = Pool(processes=num_cpus * 10)

    gdf_new = gdf.to_crs(epsg=epsg)
    print(gdf_new.crs)

    # Start processes in the pool and concat dataframes to one dataframe
    dfs = process_pool.map(
        send_requests,
        [item for item in make_centroid_sub_lists(gdf_new, chunk_size)]
    )

    df_processed = pd.concat(dfs, axis='rows', ignore_index=False)

    gdf_merged = pd.concat(
        [
            gdf_new,
            df_processed
        ],
        axis='columns',
        ignore_index=False
    )

    gdf_merged = gdf_merged.reindex(list(COL_START + COL_INFO + COL_END), axis=1)

    gdf_merged.loc[:, 'CODE'] = gdf_merged.CODE.fillna(CODE_INT_UNKNOWN)
    gdf_merged.loc[:, 'CODE'] = gdf_merged.CODE.astype(int)
    gdf_merged.columns = [col.lower() for col in gdf_merged.columns]

    print('Completed in: {} sec(s)'.format(time.time() - start))
    print(gdf_merged.info())
    print(gdf_merged.shape, gdf_merged.code.unique())
    print(gdf_merged[['code']].groupby(by='code').size().reset_index(name='counts'))

    return gdf_merged
