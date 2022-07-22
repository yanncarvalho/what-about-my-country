# -*- coding: utf-8 -*-
from config import *
import services

def create_country_fields_db():
  countries_dict = services.req_country_basic_info()
  indicators_dict = services.req_country_indicators()
  for key, val in countries_dict.items():
      services.set_country_field(key, COUNTRIES_BASIC_INFO_FIELD, val)
      if(key in indicators_dict.keys()):
        for indi, val in indicators_dict[key].items():
          services.set_country_field(key, indi, val)