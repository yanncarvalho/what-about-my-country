import helpers_convertors as conv
import helpers_req_apis as api
from django.conf import settings as conf

def req_country_basic_info() -> dict:
    countries = api.get_items_wbank_api(
        conf.WB_API_ROOT_URL, {conf.WB_COUNTRIES_INFO_URL})
    countries_dict = conv.countries_to_dict(countries)
    return countries_dict

def req_country_indicators() -> dict:
    set_indicators = {conf.WB_INDICATOR_URL + str(indicator)
                      for indicator in conf.WB_INDICATOR_KEY_API_VALUE_DICT.keys()}
    indicators = api.get_items_wbank_api(
        conf.WB_API_ROOT_URL, set_indicators)
    indicators_dict = conv.indicators_to_dict(
        indicators, conf.WB_INDICATOR_KEY_API_VALUE_DICT)
    return indicators_dict