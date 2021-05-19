#!/usr/bin/python
# -*- coding: utf-8 -*-
from deepgreen_const import *


def strip_fields(static_info, cutting_info, result):
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


def extract_static_info(response_data):
    static_info = [item.strip() for item in COMMA_LIST.split(',')]

    if str(response_data).find(STATIC_TAG) > -1:
        for response in response_data:
            _static_info = response.get(STATIC_TAG, COMMA_LIST).split(',')
            if _static_info != COMMA_LIST:
                _static_info = [item.strip() for item in _static_info]
                while len(_static_info) != len(static_info):
                    _static_info.append('')
                static_info = _static_info
            if static_info[0].strip() != '':
                break

    return static_info


def normalize_cutting_info(cutting_info):
    return [
        item.replace('</br>', '').replace('<br>', '').replace('</strong>', '').strip()
        for item in cutting_info
    ]


def extract_cutting_info(response_data):
    cutting_info = [item.strip() for item in STRONG_LIST.split('<strong>')]

    if str(response_data).find(CUTTING_TAG) > -1:
        for response in response_data:
            _cutting_info = response.get(CUTTING_TAG, STRONG_LIST).split('<strong>')
            if _cutting_info != STRONG_LIST:
                _cutting_info = normalize_cutting_info(_cutting_info)
                while len(_cutting_info) != len(cutting_info):
                    _cutting_info.append('')
                cutting_info = _cutting_info
            if cutting_info[1].strip() != '':
                break

    return cutting_info


def parse_response(response, result):
    try:
        response_data = response.get('data', [{}])
        if not isinstance(response_data, (list,)):
            result['CODE'] = CODE_INT_API_ERROR
            result['CODE_TEXT'] = CODE_TEXT_API_ERROR
        else:
            static_info = extract_static_info(response_data)
            cutting_info = extract_cutting_info(response_data)
            strip_fields(static_info, cutting_info, result)
    except Exception as err:
        result['error_msg'] = err
        result['CODE'] = CODE_INT_PARSER_ERROR
        result['CODE_TEXT'] = CODE_TEXT_PARSER_ERROR
        print('Response={} | Error={}'.format(response, err))

    return result


def normalize_cutting_url(url):
    UKR_URL = 'https://lk.ukrforest.com'
    A_HREF = "<a href='"
    try:
        return str(url).replace(A_HREF, A_HREF+UKR_URL)
    except:
        return url


def trim_pattern(value, patterns):
    REPLACE_TO = ''
    try:
        value = str(value)
        for pattern in patterns:
            value = value.replace(pattern, REPLACE_TO)
    except Exception as err:
        print(value, err)
    return value.strip()


def normalize_quarter(value):
    return trim_pattern(value, patterns=["квартал", "-"])


def normalize_square(value):
    return trim_pattern(value, patterns=["виділ", "-"])


def normalize_cutting_volume_approved(value):
    return trim_pattern(value, patterns=["Дозволений", "об'єм", "заготівлі", "-", "куб.м"])


def normalize_cutting_user(value):
    return trim_pattern(value, patterns=["Виконавець", "рубки", "-"])


def normalize_cutting_method(value):
    return trim_pattern(value, patterns=["Спосіб", "очищення", "-"])


def normalize_code_text(value):
    try:
        return str(value).replace(CODE_TEXT_LEGAL, CODE_TEXT_LEGAL_NEW).\
            replace(CODE_TEXT_LEGAL_CLOSED, CODE_TEXT_LEGAL_CLOSED_NEW). \
            replace(CODE_TEXT_LEGAL_NOT_STARTED, CODE_TEXT_LEGAL_NOT_STARTED_NEW). \
            replace(CODE_TEXT_NOT_LEGAL, CODE_TEXT_NOT_LEGAL_NEW). \
            replace(CODE_TEXT_NOT_IDENTIFIED, CODE_TEXT_NOT_IDENTIFIED_NEW). \
            replace(CODE_TEXT_API_ERROR, CODE_TEXT_API_ERROR_NEW)
    except:
        return value


def normalize_data(gdf):
    gdf.quarter = gdf.quarter.apply(normalize_quarter)
    gdf.square = gdf.square.apply(normalize_square)
    gdf.cutting_ticket_url = gdf.cutting_ticket_url.apply(normalize_cutting_url)
    gdf.cutting_user = gdf.cutting_user.apply(normalize_cutting_user)
    gdf.cutting_method = gdf.cutting_method.apply(normalize_cutting_method)
    gdf.cutting_volume_approved = gdf.cutting_volume_approved.apply(normalize_cutting_volume_approved)
    gdf.code_text = gdf.code_text.apply(normalize_code_text)
    # gdf.coords = gdf.centroid
    return gdf