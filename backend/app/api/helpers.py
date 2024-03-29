"""Helpers functions"""
import asyncio
import re
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
import logging
import aiohttp
from django.conf import settings as conf

CountryAPIRequest = Dict[str, Union[int, float, str]]

def _sanitize_string(value: str) -> str:
    """ Remove unnecessary caracteries and change words

    Args:
    - value: String that will be sanitize

    Returns:
      String sanitized
    """
    value = value.strip()

    rule: str = lambda val: re.sub(r'\s*[SAR]*\s*,.*', '', val)
    exceptions: Dict[str, str] = {
        "Congo, Dem. Rep.": "Democratic Republic of the Congo",
        "Congo, Rep.": "Republic of the Congo",
        "Korea, Dem. People's Rep.": "Democratic People's Republic of Korea (North Korea)",
        "Korea, Rep.": "Republic of Korea (South Korea)",
        "Bahamas, The": "The Bahamas",
        "Population, total": "Total population",
        "Lao PDR": "Lao People's Democratic Republic (Laos)",
        "St. Vincent and the Grenadines": "Saint Vincent and the Grenadines",
        "St. Lucia": "Saint Lucia",
        "St. Kitts and Nevis": "Saint Kitts and Nevis"
    }
    return exceptions[value] if value in exceptions else rule(value)


def _indicators_normalize(indicators: List[Dict[str, str]],
                          indicatorapi_dictkey: Dict[str, str]) -> Dict[str, CountryAPIRequest]:
    """ Convert a list of indicators from World Bank API into a dictionary with filtered elements

    Args:
    - indicators: list of indicators with World Bank API informations
        Bbasic indicator structure:\n
        [{
            'indicator':{'value', 'id'},\n
            'value',\n
            'date',\n
        }]\n

    - indicatorapi_dictkey: a dictionary where the key is World Bank API ID
                            and the value is the ID of the local indicator,
                            which will represent information to populate the local database

    Returns:
      A dictionary with filtered and rearranged indicators information,
      whose each dictionary key is the ID of the local indicator
    """
    result: Dict[str, CountryAPIRequest] = {}
    for indi in indicators:
        try:
            value: int = indi['value']
            if value:
                description: str = _sanitize_string(indi['indicator']['value'])
                key: str = '/'.join((conf.API_INDICATOR_URL,
                                    indi['indicator']['id']))
                indicator: str = indicatorapi_dictkey[key]

                if indicator not in result:
                    result.update({
                        indicator: {
                            'id': indicator,
                            'description': description,
                            'data': []
                        }
                    })

                result[indicator]['data'].append({
                    'year': int(indi['date']),
                    'value': value
                })
        except RuntimeError as err:
            logging.error('Could not normalize %s - %s', indi, err)
    return result


def _is_valid_country(country: CountryAPIRequest) -> bool:
    """ Check if a country is valid

    Args:
    - country: a dictionary with country information

    Returns:
      True if the country is valid, False if not
    """
    basic_data: Set[str] = {'iso2Code',
                            'name',
                            'region',
                            'capitalCity',
                            'longitude',
                            'latitude',
                            'incomeLevel'}

    if has_basic_data := basic_data.issubset(set(country.keys())):
        has_value_in_keys = 'value' in set(country['region'].keys()).intersection(
            set(country['incomeLevel'].keys()))
        is_country = country['incomeLevel']['value'] != 'Aggregates' and country['longitude'] != ''
    return has_basic_data and has_value_in_keys and is_country


def _country_basic_info_normalize(country: CountryAPIRequest,
                                  field_name: str) -> Dict[str, CountryAPIRequest]:
    """
      Convert a dictionary with basic world bank country
      information to a dictionary with filtered elements

    Args:
    - Countries: list of dictionary with countries with all information from World Bank API
        Basic structure of the country dictionary:\n
        [{
            'iso2Code',\n
            'name',\n
            'region':{'value'},\n
            'capitalCity',\n
            'longitude',\n
            'latitude',\n
            'incomeLevel': {value}\n
        }]\n
    - field_name: key which will represent basic country information
                  that will be used to populate the local database

    Returns:
      A dictionary where the key is field_name paramater
      and its value is a dictionary with filtered basic country information
    """
    try:
        result: Dict[str, CountryAPIRequest] = \
            {field_name: {
                'id': _sanitize_string(country['iso2Code']),
                'name': _sanitize_string(country['name']),
                'region': _sanitize_string(country['region']['value']),
                'capitalCity': _sanitize_string(country['capitalCity']),
                'longitude': float(country['longitude']),
                'latitude': float(country['latitude']),
                'incomeLevel': _sanitize_string(country['incomeLevel']['value']),
            }}
    except RuntimeError as err:
        logging.error('Could not normalize country %s - %s', country,  err)
    return result


async def _request_wbank_api(session: aiohttp.ClientSession,
                             api_url_base: str,
                             req: str,
                             per_page: int) -> List[CountryAPIRequest]:
    """ Access the World bank API and the number of elements in a specific endpoint

    Args:
    - session: aiohttp.ClientSession session value to create connection to World Bank API
    - api_url_base: base with World Bank API url
    - req: request that will be made into World Bank API
    - per_page: how many elements per page will be request

    Returns:
      A list of element converted from a json if got response, otherwise an empty list
    """
    try:
        url = f"https://{api_url_base}/{req}?format=Json&per_page={per_page}"
        async with session.get(url) as resp:
            json_resp = await resp.json()
            logging.info('requesting url: %s', url)
            return json_resp
    except RuntimeError as err:
        logging.error('error trying to request %s - %s', url, err)


async def _get_items_wbank_api(api_url_base: str,
                              requests: Sequence[str]) -> List[CountryAPIRequest]:
    """ Access World Bank API and return a list all elements required

    Args:
    - api_url_base: World Bank API base URL
    - request: a sequence with all requests that will be made to the World Bank API

    Returns:
      A list with all required elements which got a response,
      in case of no response, returns an empty list
    """
    result: List[CountryAPIRequest] = []
    async with aiohttp.ClientSession() as session:
        for req in requests:
            try:
                amount_items: List[CountryAPIRequest] = \
                    await _request_wbank_api(session, api_url_base, req, per_page=1)
                per_page: int = amount_items[0]['total']
                data: List[CountryAPIRequest] = \
                    await _request_wbank_api(session, api_url_base, req, per_page)
                result += data[1]
            except RuntimeError as err:
                logging.error('error trying to reques: %s  - %s', req, err)

    return result


def get_keys_n_name_from_net() -> Tuple[Dict[str, str]]:
    """ Request to World Bank API basic countries information and
    return them iso2Code IDs and country names

    Returns:
     A tuple of dictionaries with:\n
     {
      \tid: country iso2Code ID
      \tname: country name\n
     }
    """
    api_url_root: str = conf.API_URL_ROOT
    country_url: str = conf.API_COUNTRY_URL
    countries_n_regions: List[CountryAPIRequest] = asyncio.run(
        _get_items_wbank_api(api_url_root, {country_url}))

    countries_keys_n_name: Tuple[str, Dict[str, str]] = \
        tuple({'id': val['iso2Code'], 'name': _sanitize_string(val['name'])}
              for val in countries_n_regions
              if _is_valid_country(val))
    return countries_keys_n_name


async def get_from_net(key: str) -> Optional[CountryAPIRequest]:
    """ request basic country information from the World Bank API and returns iso2Code IDs

    Args:
    - key: country iso2Code ID

    Returns:
      A dictionary with information for a specific country,
      if the country key does not come out, it returns and the dictionary is empty

    Raises:
      ValueError: An error ocorred if the key is not a String or is an empty string
    """
    if not isinstance(key, str) or key.replace(' ', '') == '':
        logging.critical('code "%s" must be a string with some character', key)
        raise ValueError('code must be a string with some character')

    api_url_root: str = conf.API_URL_ROOT
    country_url: str = conf.API_COUNTRY_URL
    basic_info_id: str = conf.API_BASIC_INFO_URL
    from_net_to_dict: Dict[str, str] = {
        k: v['id'] for k, v in conf.FROM_NET_KEY_TO_DICT_VALUE.items()}

    urls: List[str] = {indicator: '/'.join((country_url, key, str(indicator)))
                       for indicator in from_net_to_dict.keys()}
    index_basic_info: int = list(urls.keys()).index(basic_info_id)

    if urls:

        country = await _get_items_wbank_api(api_url_root, list(urls.values()))

        if bool(country):
            basic_info: Dict[str, object] = country.pop(index_basic_info)

            country_normalized: Dict[str, CountryAPIRequest] =\
                _country_basic_info_normalize(
                    basic_info, from_net_to_dict[basic_info_id])

            if len(country) >= 1:
                infos_filtered: Dict[str, CountryAPIRequest] = _indicators_normalize(
                    country, from_net_to_dict)
                country_normalized.update(infos_filtered)

            return country_normalized
