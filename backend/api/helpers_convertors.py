import re

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

def indicators_to_dict(indicators: list, indicatorApi_dictKey: dict) -> dict:
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
                                                'data': {}
                                            }
                                        }
                                      )
      result[country_code][indicator]['data'].update({indi['date']: value})
  return result

def countries_to_dict(countries: list) -> dict:
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
          aux = {
              'id': info['iso2Code'],
              'name': _sanitize_string(info['name']),
              'region': _sanitize_string(info['region']['value']),
              'capitalCity': _sanitize_string(info['capitalCity']),
              'longitude': float(info['longitude']),
              'latitude': float(info['latitude']),
              'incomeLevel': _sanitize_string(info['incomeLevel']['value']),
          }
          result.update({aux['id']:aux})
  except Exception:
      raise Exception('countries do not have all elements necessary')
  return result