import json
import re
from http import client
from http.client import HTTPSConnection
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
      country_code = indi['country']['id']
      description = _sanitize_string(indi['indicator']['value'])
      indicator = indicatorApi_dictKey[indi['indicator']['id']]

      if(country_code not in result.keys()):
          result[country_code]: dict = {}

      if(indicator not in result[country_code].keys()):
          result[country_code].update(
                                        {
                                            indicator: {
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


def _countries_filtered(countries: list, field_name: str) -> dict:
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
    FILTERD Dict of countries informations from world bank where key are iso2code

  Raises:
    Exception: if countries do not have the basic struct."""
  try:
    result: dict = {}
    for info in countries:
      if(info['incomeLevel']['value'] != 'Aggregates' and info['longitude'] != ''):
          id = info['iso2Code']
          aux = {
              field_name: {
              'name': _sanitize_string(info['name']),
              'region': _sanitize_string(info['region']['value']),
              'capitalCity': _sanitize_string(info['capitalCity']),
              'longitude': float(info['longitude']),
              'latitude': float(info['latitude']),
              'incomeLevel': _sanitize_string(info['incomeLevel']['value']),
            }
          }
          result.update({id : aux})
  except Exception:
      raise Exception('countries do not have all elements necessary')
  return result


def _get_endpoint_wbank_itens_amount(conn: HTTPSConnection, request: str, http_method: str = 'GET') -> int:
    """Access the World bank API and the number of elements in a specific endpoint"""
    conn.request(http_method, f"/{request}?format=Json&per_page=1")
    response = conn.getresponse().read().decode()
    data = json.loads(response)
    return data[0]['total']


def _get_items_wbank_api(urlBaseApiHttps: str, requests: list, http_method: str = 'GET') -> list:
    """ Access the World Bank API and return a tuple with request data at first element are data requited and second one is the last update of the API"""
    conn = client.HTTPSConnection(urlBaseApiHttps)
    result: list = []
    for req in requests:
        per_page = _get_endpoint_wbank_itens_amount(conn, req, http_method)
        conn.request(http_method, f"/{req}?format=Json&per_page={per_page}")
        response = conn.getresponse().read().decode()
        json_resp = json.loads(response)
        data = json_resp[1]
        print("get world bank information from country iso2code ", req)
        result += data
    conn.close()
    return result


def get_keys_from_net() -> set:
  api_url_root: str = conf.API_URL_ROOT
  country_url: str = conf.API_COUNTRY_URL
  basic_info: str = conf.BASIC_INFO_FIELD

  countries_n_regions: list = _get_items_wbank_api(api_url_root, {country_url})
  countries: dict = _countries_filtered( countries_n_regions, basic_info)
  return set(countries.keys())

def get_from_net(iso2code: str = '') -> dict:
  api_url_root: str = conf.API_URL_ROOT
  country_url: str = conf.API_COUNTRY_URL
  indicator_url: str = conf.API_INDICATOR_URL
  basic_info: str = conf.BASIC_INFO_FIELD
  from_net_to_field: dict  = conf.FROM_NET_KEY_TO_FIELD_VALUE

  countries_n_regions: list = _get_items_wbank_api( api_url_root, {'/'.join((country_url,iso2code))})

  countries: dict = _countries_filtered(countries_n_regions, basic_info)

  for key in countries.keys():

      urls: set = {'/'.join((country_url, key, indicator_url, str(indicator)))
                   for indicator in from_net_to_field.keys()}
      if urls:
        country_infos = _get_items_wbank_api(api_url_root, urls)
        infos_filter = _infos_filtered(
            country_infos, from_net_to_field)
        countries[key].update(infos_filter[key])
  return countries