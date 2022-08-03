import asyncio
import re
from typing import *
import aiohttp
from django.conf import settings as conf

def _sanitize_string(value: str) -> str:
  value = value.strip()

  rule: str = lambda val: re.sub('\s*[SAR]*\s*,.*', '', val)
  exceptions: Dict[str, str] = {
    "Congo, Dem. Rep.": "Democratic Republic of the Congo",
    "Congo, Rep.": "Republic of the Congo",
    "Korea, Dem. People's Rep.": "Democratic People's Republic of Korea (North Korea)",
    "Korea, Rep.": "Republic of Korea (South Korea)",
    "Bahamas, The": "The Bahamas",
    "Population, total" : "Total population",
    "Lao PDR": "Lao People's Democratic Republic (Laos)",
    "St. Vincent and the Grenadines": "Saint Vincent and the Grenadines",
    "St. Lucia": "Saint Lucia",
    "St. Kitts and Nevis": "Saint Kitts and Nevis"
  }
  return exceptions[value] if value in exceptions.keys() else rule(value)


def _indicators_normalize(indicators: List[Dict[str, str]],
                         indicatorApi_dictKey: Dict[str, str]) -> Dict[str, Dict[str, object]]:
  result: Dict[str, object] = {}
  for indi in indicators:
    try:
      value: int = indi['value']
      if value:
        description: str = _sanitize_string(indi['indicator']['value'])
        key: str = '/'.join((conf.API_INDICATOR_URL, indi['indicator']['id']))
        indicator: str = indicatorApi_dictKey[key]

        if(indicator not in result.keys()):
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
    except Exception:
        print('It was not able to normalize '+ indi)
  return result

def _is_valid_country(country: Dict[str, str]) -> bool:
  basic_data: Set[str] = {'id',
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

def _country_basic_info_normalize(country: Dict[str, object], field_name: str) -> Dict[str, Dict[str, Union[str, float]]]:
  try:
   result: Dict[str, Dict[str, object]] = \
           {field_name: {
                 'id': _sanitize_string(country['id']),
                 'name': _sanitize_string(country['name']),
                 'region': _sanitize_string(country['region']['value']),
                 'capitalCity': _sanitize_string(country['capitalCity']),
                 'longitude': float(country['longitude']),
                 'latitude': float(country['latitude']),
                 'incomeLevel': _sanitize_string(country['incomeLevel']['value']),
             }}
  except Exception:
        pass
  return result

async def _request_wbank_api(session: aiohttp.ClientSession,
                            urlBaseApiHttps: str,
                            req: str,
                            per_page: int) -> List[object]:
  try:
    url = f"https://{urlBaseApiHttps}/{req}?format=Json&per_page={per_page}"
    async with session.get(url) as resp:
        json_resp = await resp.json()
        return json_resp
  except Exception:
    pass

async def _get_items_wbank_api(urlBaseApiHttps: str, requests: Sequence[str]) -> List[Dict[str, str]]:
  result: List[object] = []
  async with aiohttp.ClientSession() as session:
    for req in requests:
      try:
        amount_items: List[object] = await _request_wbank_api(session, urlBaseApiHttps, req, per_page=1)
        per_page: int = amount_items[0]['total']
        data: List[object] = await _request_wbank_api(session, urlBaseApiHttps, req, per_page)
        result += data[1]
      except Exception:
        pass
  return result

def get_keys_from_net() -> Set[str]:
  api_url_root: str = conf.API_URL_ROOT
  country_url: str = conf.API_COUNTRY_URL
  countries_n_regions: List[Dict[str, str]] = asyncio.run(_get_items_wbank_api(api_url_root, {country_url}))
  countries_keys: Set[str] = {val['id'] for val in countries_n_regions
                                        if _is_valid_country(val)}
  return countries_keys

async def get_from_net(key: str) -> Dict[str, Dict[str, object]]:
  if not isinstance(key, str) or key.replace(' ', '') == '':
      raise ValueError('code has be a string with some character')

  api_url_root: str = conf.API_URL_ROOT
  country_url: str = conf.API_COUNTRY_URL
  basic_info_id: str = conf.API_BASIC_INFO_URL
  from_net_to_dict: Dict[str, str] = conf.FROM_NET_KEY_TO_DICT_VALUE

  urls: List[str] = {indicator: '/'.join((country_url, key, str(indicator)))
                     for indicator in from_net_to_dict.keys()}
  index_basic_info: int = list(urls.keys()).index(basic_info_id)
  country_normalized: Dict[str, Dict[str, object]] = {}

  if urls:
    country = await _get_items_wbank_api(api_url_root, list(urls.values()))
    if bool(country):
      basic_info: Dict[str, object] = country.pop(index_basic_info)
      country_normalized = \
          _country_basic_info_normalize(basic_info, from_net_to_dict[basic_info_id])
      if len(country) >= 1:
        infos_filtered: Dict[str, Dict[str, object]] = _indicators_normalize(country, from_net_to_dict)
        country_normalized.update(infos_filtered)
  return country_normalized