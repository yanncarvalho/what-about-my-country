# -*- coding: utf-8 -*-
import json
import redis
from config import COUNTRIES_BASIC_INFO_FIELD
from models import Country, Field

_ID_COUNTRY_REFERENCE: str = 'iso2code'+':'

redis = redis.Redis(port=6379,  charset="utf-8", decode_responses=True)

def get_countries_ids() -> list:
  return [key.replace(_ID_COUNTRY_REFERENCE, '') for key in redis.keys(_ID_COUNTRY_REFERENCE+':*')]

def get_country(iso2code: str) -> Country:
  elems_serialized: dict = redis.hgetall(_ID_COUNTRY_REFERENCE+iso2code)
  elems_deserialized: dict = {key: Field(key, json.loads(val))
                              for key, val in elems_serialized.items()}
  basic_info: dict = elems_deserialized.pop(COUNTRIES_BASIC_INFO_FIELD).get_info()
  indicators: dict = elems_deserialized
  return Country(iso2code, basic_info, indicators)

def get_country_field(iso2code: str, field_id: str) -> Field:
  info: dict = json.loads(redis.hget(_ID_COUNTRY_REFERENCE+iso2code, field_id))
  return Field(field_id, info)

def set_country_field(iso2code: str, field: Field) -> None:
  redis.hset(_ID_COUNTRY_REFERENCE+iso2code, field.get_id(), json.dumps(field.get_info()))