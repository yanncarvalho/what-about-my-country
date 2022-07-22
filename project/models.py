# -*- coding: utf-8 -*-

class Field():
  def __init__(self, field_id: str, info: dict):
    self._id = field_id
    self._info = info

  def get_info(self) -> dict:
    return self._info

  def get_id(self) -> str:
    return self._id

  def __str__(self) -> str:
    return f'{self._info}'

  def __repr__(self):
    return f'{self._info}'

class Country():
  def __init__(self, country_code: str, basic_info: dict, indicators: dict):
    self._country_code = country_code
    self._basic_info = basic_info
    self._indicators = indicators

  def get_indicators(self) -> dict:
    return self._indicators

  def get_indicator(self, indi_id:str) -> dict:
    if(indi_id in self._indicators.keys()):
      return self._indicators[indi_id]
    else:
      return None

  def get_basic_info(self) -> str:
    return self._basic_info

  def get_country_code(self) -> str:
    return self._country_code

  def __str__(self) -> str:
    return f'basic_info: {self._basic_info} - indicators: {self._indicators}'

  