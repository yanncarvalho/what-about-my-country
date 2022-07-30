import json
import redis
from django.conf import settings
from .observer import ObserverDB

redis = redis.Redis(port=settings.REDIS['port'],
                    charset=settings.REDIS['charset'],
                    decode_responses=settings.REDIS['decode_responses'])

class Field:

  def __init__(self, field_id: str, info: dict):
    self.__id = field_id
    self.__info = info

  @property
  def info(self) -> dict:
    return self.__info

  @property
  def id(self) -> str:
    return self.__id

  def __str__(self) -> str:
    return f'{self.__info}'

  def __repr__(self) -> str:
    return f'{self.__info}'

class RedisModel(ObserverDB):

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
    dict_field = {field.id: json.dumps(field.info) for field in fields}
    redis.hmset(self.__key, mapping=dict_field)
    super().save()

  def delete(self) -> None:
    redis.delete(self.__key)

  @staticmethod
  def del_keys_by_pattern(pattern: str) -> None:
    for key in redis.scan_iter(pattern+":*"):
      redis.delete(key)

  @staticmethod
  def all_keys(id_reference: str) -> list:
    id_reference = id_reference + ':'
    return [key.replace(id_reference, '') for key in redis.scan_iter(id_reference+'*')]
