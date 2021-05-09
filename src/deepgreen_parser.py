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
