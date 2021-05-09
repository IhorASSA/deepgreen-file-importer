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
CODE_INT_LEGAL_CLOSED = 2
CODE_TEXT_LEGAL_CLOSED = 'Легальна закрита'
CODE_INT_LEGAL_NOT_STARTED = 3
CODE_TEXT_LEGAL_NOT_STARTED = 'Легальна не розпочата'
CODE_INT_NOT_LEGAL = 4
CODE_TEXT_NOT_LEGAL = 'Нелегальна відсутній лісорубний'
CODE_INT_NOT_IDENTIFIED = 5
CODE_TEXT_NOT_IDENTIFIED = 'Проблеми ідентифікації місцерозташування'
CODE_INT_UNKNOWN_RUBKA = 6
CODE_TEXT_UNKNOWN_RUBKA = 'Рубка - невідомий сценарій'
CODE_INT_PARSER_ERROR = 7
CODE_TEXT_PARSER_ERROR = 'DeepGreen Parser Error'
CODE_INT_API_ERROR = 8
CODE_TEXT_API_ERROR = 'UkrForest API Error'
CODE_INT_UNKNOWN = 9
CODE_TEXT_UNKNOWN = 'Unknown Error'

# PG_TABLE_NAME='pg_deepgreen_demo_arsen'
# PG_DB_CONNECTION_STRING="postgresql://deepgreen:HJKj4oiIUs-8@ec2-52-204-66-46.compute-1.amazonaws.com:5432/deepgreen"
#PG_DB_CONNECTION_STRING="postgresql://deepgreen:deepgreen2021MT!@ec2-15-188-127-126.eu-west-3.compute.amazonaws.com:5432/deepgreen"
#PG_DB_CONNECTION_STRING="postgresql://deepgreen:deepgreen2021MT!@localhost:5432/deepgreen"
PG_DB_CONNECTION_STRING="postgresql://deepgreen:deepgreen2021MT!@deepgreen.ccameumzy8wt.us-east-1.rds.amazonaws.com:5432/deepgreen"
PG_TABLE_NAME = 'spatial_data_new'
