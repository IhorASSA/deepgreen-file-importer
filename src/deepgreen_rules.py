#!/usr/bin/python
# -*- coding: utf-8 -*-
from deepgreen_const import *


def set_rules_ver02(result):
    """
      Rules prepared for DEMO-1 by Sash
    """
    if result['region'] != '':
        if CUT_STATUS_STARTED in result['cutting_status']:  # Legal
            result['CODE'] = 1
            result['CODE_TEXT'] = 'Легальна'
        elif CUT_STATUS_CLOSED in result['cutting_status']:  # Not Legal
            result['CODE'] = 2
            result['CODE_TEXT'] = 'Не легальна (Рубка - Закрита)'
        elif CUT_STATUS_NOT_STARTED in result['cutting_status']:  # Not Legal | Don't started
            result['CODE'] = 3
            result['CODE_TEXT'] = 'Не легальна (Рубка - Не розпочата)'
        else:
            result['CODE'] = 5  # Unknown case
            result['CODE_TEXT'] = 'Невідомий сценарій'
    else:
        result['CODE'] = 4  # User is not identified
        result['CODE_TEXT'] = 'Не ідентифікований лісокористувач'

    return result


def set_rules_ver03(result):
    """
      Rules prepared for DEMO-2 by Client&Team
    """
    if result['region'] != '':
        if CUT_STATUS_STARTED in result['cutting_status']:  # Legal
            result['CODE'] = CODE_INT_LEGAL
            result['CODE_TEXT'] = CODE_TEXT_LEGAL
        elif CUT_STATUS_CLOSED in result['cutting_status']:  # Legal "Closed"
            result['CODE'] = CODE_INT_LEGAL_CLOSED
            result['CODE_TEXT'] = CODE_TEXT_LEGAL_CLOSED
        elif CUT_STATUS_NOT_STARTED in result['cutting_status']:  # Legal "Don't started"
            result['CODE'] = CODE_INT_LEGAL_NOT_STARTED
            result['CODE_TEXT'] = CODE_TEXT_LEGAL_NOT_STARTED
        elif CUT_NAME in result['cutting_status']:
            result['CODE'] = CODE_INT_UNKNOWN_RUBKA  # Unknown case - "Rubka Karl", simply 'Rubka'
            result['CODE_TEXT'] = CODE_TEXT_UNKNOWN_RUBKA
        else:
            result['CODE'] = CODE_INT_NOT_LEGAL  # Not Legal
            result['CODE_TEXT'] = CODE_TEXT_NOT_LEGAL
    else:
        result['CODE'] = CODE_INT_NOT_IDENTIFIED  # Place is not identified
        result['CODE_TEXT'] = CODE_TEXT_NOT_IDENTIFIED

    return result
