# -*- coding: utf-8 -*-

import json
import redis
from django.conf import settings

redis = redis.Redis(port=settings.REDIS['port'],
                    charset=settings.REDIS['charset'],
                    decode_responses=settings.REDIS['decode_responses'])

class Field:

  def __init__(self, field_id: str, info: dict):
    self._id = field_id
    self._info = info

  @classmethod
  def get_info(self) -> dict:
    return self._info

  @classmethod
  def get_id(self) -> str:
    return self._id

class RedisModel:

  def __init__(self, key: str, id_reference: str) -> None:
    self.id_reference = id_reference
    self.key = self.id_reference+key

  @classmethod
  def get_fields(self) -> dict:
    elems_serialized: dict = redis.hgetall(self.key)
    elems_deserialized: dict = {key: Field(key, json.loads(val))
                                for key, val in elems_serialized.items()}
    return elems_deserialized

  @classmethod
  def get_field(self, field_id: str) -> Field:
    info: dict = json.loads(redis.hget(
       self.key, field_id))
    return Field(field_id, info)

  @classmethod
  def save_field(self, field: Field) -> None:
    redis.hset(self.key,
             field.get_id(), json.dumps(field.get_info()))

  @staticmethod
  def all_keys(id_reference: str) -> list:
    return [key.replace(id_reference, '') for key in redis.keys(id_reference+':*')]
