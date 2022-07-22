# -*- coding: utf-8 -*-
import project.helpers_convertors as conv
import project.helpers_req_apis as api
from config import *

def req_country_basic_info() -> dict:
    countries = api.get_items_wbank_api(
        WB_API_ROOT_URL, {WB_COUNTRIES_INFO_URL})
    countries_dict = conv.countries_to_dict(countries)
    return countries_dict


def req_country_indicators() -> dict:
    set_indicators = {WB_INDICATOR_URL + str(indicator)
                      for indicator in WB_INDICATOR_KEY_API_VALUE_DICT.keys()}
    indicators = api.get_items_wbank_api(
        WB_API_ROOT_URL, set_indicators)
    indicators_dict = conv.indicators_to_dict(
        indicators, WB_INDICATOR_KEY_API_VALUE_DICT)
    return indicators_dict
