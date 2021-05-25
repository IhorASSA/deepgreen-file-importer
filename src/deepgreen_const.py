import logging as logger

logger.basicConfig(
    filename="log_file_test.log",
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logger.DEBUG
)
logger.info("This is a test log ..")

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
    'centroid': [],
    'raw_response': {},
    'url': None,
    'error_msg': ''
}

COMMA_LIST = ', ' * 3
STRONG_LIST = '<strong> ' * 4

STATIC_TAG = 'static'
CUTTING_TAG = 'cutting'

CUT_NAME = 'Рубка'
CUT_STATUS_STARTED = 'Рубка - Розпочата'
CUT_STATUS_CLOSED = 'Рубка - Закрита'
CUT_STATUS_NOT_STARTED = 'Рубка - Не розпочата'

COL_START = ['datetime', 'ID', 'CODE', 'CODE_TEXT', 'area', 'Extend', 'geometry']
COL_INFO = ['region', 'district', 'quarter', 'square',
            'cutting_ticket_url', 'cutting_status', 'cutting_volume_approved',
            'cutting_user', 'cutting_method']
COL_END = ['url', 'coords',	'raw_response', 'error_msg']

CODE_INT_LEGAL = 1
CODE_TEXT_LEGAL = 'Легальна діюча'
CODE_TEXT_LEGAL_NEW = 'Легальна діюча рубка'
CODE_INT_LEGAL_CLOSED = 2
CODE_TEXT_LEGAL_CLOSED = 'Легальна закрита'
CODE_TEXT_LEGAL_CLOSED_NEW = 'Легальна закрита рубка'
CODE_INT_LEGAL_NOT_STARTED = 3
CODE_TEXT_LEGAL_NOT_STARTED = 'Легальна не розпочата'
CODE_TEXT_LEGAL_NOT_STARTED_NEW = 'Легальна не розпочата рубка'
CODE_INT_NOT_LEGAL = 4
CODE_TEXT_NOT_LEGAL = 'Нелегальна відсутній лісорубний'
CODE_TEXT_NOT_LEGAL_NEW = 'Нелегальна відсутній лісорубний квиток'
CODE_INT_NOT_IDENTIFIED = 5
CODE_TEXT_NOT_IDENTIFIED = 'Проблеми ідентифікації місцерозташування'
CODE_TEXT_NOT_IDENTIFIED_NEW = 'Проблеми ідентифікації місцерозташування рубки'
CODE_INT_UNKNOWN_RUBKA = 6
CODE_TEXT_UNKNOWN_RUBKA = 'Рубка - невідомий сценарій'
CODE_INT_PARSER_ERROR = 7
CODE_TEXT_PARSER_ERROR = 'DeepGreen Parser Error'
CODE_INT_API_ERROR = 8
CODE_TEXT_API_ERROR = 'UkrForest API Error'
CODE_TEXT_API_ERROR_NEW = 'UkrForest API Error'
CODE_INT_UNKNOWN = 9
CODE_TEXT_UNKNOWN = 'Unknown Error'

import os
from dotenv import load_dotenv,dotenv_values

path = ".env" + (("." + os.getenv('APP_ENV')) if os.getenv('APP_ENV') else "")
#print("Loading config from path:" + path)
env = dotenv_values(path)
#print(env)

PG_DB_CONNECTION_STRING = env['PG_DB_CONNECTION_STRING']
PG_TABLE_NAME = env['PG_TABLE_NAME']
