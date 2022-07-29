import asyncio
import json
import re
from http import client
from http.client import HTTPSConnection


import aiohttp
from django.conf import settings as conf


def _sanitize_string(str:str) -> str:
  """Remove unnecessary caracteries or change words"""
  str = str.strip()

  rule = lambda string: re.sub('\s*[SAR]*\s*,.*', '', string)

  exceptions = {
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

  return exceptions[str] if str in exceptions.keys() else rule(str)


def _infos_filtered(indicators: list, indicatorApi_dictKey: dict) -> list:
  """Convert list of indicators from world bank into a dictionary"""
  result = {}
  for indi in indicators:
    value = indi['value']
    if(value != None):
      country_code = indi['countryiso3code']
      description = _sanitize_string(indi['indicator']['value'])
      indicator = indicatorApi_dictKey[indi['indicator']['id']]

      if(country_code not in result.keys()):
          result[country_code]: dict = {}

      if(indicator not in result[country_code].keys()):
          result[country_code].update(
                                        {
                                            indicator: {
                                                'id': indicator,
                                                'description': description,
                                                'data': []
                                            }
                                        }
                                      )

      result[country_code][indicator]['data'].append({
                                                      'year': int(indi['date']),
                                                      'value': value
                                                     })
  return result

def _is_valid_country(country: dict) -> bool:
  basic_data = {'id',
                'name',
                'region',
                'capitalCity',
                'longitude',
                'latitude',
                'incomeLevel'}


  has_basic_data = basic_data.issubset(set(country.keys()))
  has_value_in_keys = 'value' in country['region'].keys() and 'value' in country['incomeLevel'].keys()
  is_a_country = country['incomeLevel']['value'] != 'Aggregates' and country['longitude'] != ''
  return has_basic_data and has_value_in_keys and is_a_country



def _country_normalize(country: dict, field_name: str) -> dict:
  """Dict of countries informations from world bank where key are iso2code.

  Args:
    Countries: list of dictionary with countries with all information from wb API
    Country dictionary basic struct:\n
      [{
          'iso2Code',\n
          'name',\n
          'region':{'value'},\n
          'capitalCity',\n
          'longitude',\n
          'latitude',\n
          'incomeLevel': {value}\n
      }]\n

  Returns:
    FILTERD Dict of countries informations from world bank where key are

 """

  result = { field_name: {
                'id': _sanitize_string(country['id']),
                'name': _sanitize_string(country['name']),
                'region': _sanitize_string(country['region']['value']),
                'capitalCity': _sanitize_string(country['capitalCity']),
                'longitude': float(country['longitude']),
                'latitude': float(country['latitude']),
                'incomeLevel': _sanitize_string(country['incomeLevel']['value']),
            } }

  return result



async def _get_endpoint_wbank_itens_amount(session, url_base: str) -> int:
    """Access the World bank API and the number of elements in a specific endpoint"""
    url = f"{url_base}&per_page=1"
    async with session.get(url) as resp:
        json_resp = await resp.json()
        return json_resp[0]['total']

async def _get_items_wbank_api(urlBaseApiHttps: str, requests: list) -> list:
    """ Access the World Bank API and return a tuple with request data at first element are data requited and second one is the last update of the API"""
    result: list = []

    async with aiohttp.ClientSession() as session:

      for req in requests:
          url_base = f"https://{urlBaseApiHttps}/{req}?format=Json"
          per_page = await _get_endpoint_wbank_itens_amount(session, url_base)
          url = f"{url_base}&per_page={per_page}"
          async with session.get(url) as resp:
            json_resp = await resp.json()
            data = json_resp[1]
            result += data
    return result


def get_keys_from_net() -> set:
  api_url_root: str = conf.API_URL_ROOT
  country_url: str = conf.API_COUNTRY_URL

  countries_n_regions: list = asyncio.run(_get_items_wbank_api(api_url_root, {country_url}))
  countries_keys = {val['id'] for val in countries_n_regions
                    if _is_valid_country(val)}

  return countries_keys


async def get_from_net(key: str) -> dict:

  if type(key) != str or key == '':
      raise Exception('code has be a string, with some caracter')
  print(key)
  api_url_root: str = conf.API_URL_ROOT
  country_url: str = conf.API_COUNTRY_URL
  indicator_url: str = conf.API_INDICATOR_URL
  basic_info: str = conf.BASIC_INFO_FIELD
  from_net_to_field: dict  = conf.FROM_NET_KEY_TO_FIELD_VALUE

  country: dict = (await _get_items_wbank_api(api_url_root, {'/'.join((country_url, key))}))[0]
  country_filtered: dict = _country_normalize(country, basic_info)

  urls: set = {'/'.join((country_url, key, indicator_url, str(indicator)))
               for indicator in from_net_to_field.keys()}

  if urls:
    country_infos = await _get_items_wbank_api(api_url_root, urls)
    infos_filter = _infos_filtered(country_infos, from_net_to_field)
    country_filtered.update(infos_filter[key])

  return country_filtered

