import json

import redis
from django.conf import settings

redis = redis.Redis(port=settings.REDIS['port'],
                    charset=settings.REDIS['charset'],
                    decode_responses=settings.REDIS['decode_responses'])

class Field:

  def __init__(self, field_id: str, info: dict):
    self.__id = field_id
    self.__info = info

  def get_info(self) -> dict:
    return self.__info

  def get_id(self) -> str:
    return self.__id

  def __str__(self) -> str:
    return f'{self.__info}'

  def __repr__(self) -> str:
    return f'{self.__info}'

class RedisModel:

  def __init__(self, key: str) -> None:
     self.__key = key

  def get_fields(self) -> dict:
    elems_serialized: dict = redis.hgetall(self.__key)
    elems_deserialized: dict = {key: Field(key, json.loads(val))
                                for key, val in elems_serialized.items()}
    return elems_deserialized

  def get_field(self, field_id: str) -> Field:
    info: dict = json.loads(redis.hget(
        self.__key, field_id))
    return Field(field_id, info)

  def save(self, fields: list) -> None:
    for field in fields:
      redis.hset(self.__key,
               field.get_id(), json.dumps(field.get_info()))

  @staticmethod
  def all_keys(id_reference: str) -> list:
    id_reference = id_reference + ':'
    return [key.replace(id_reference, '') for key in redis.keys(id_reference+'*')]
