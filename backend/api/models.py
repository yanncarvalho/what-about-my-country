import json
from typing import Any, Dict, List

from .observer import ObserverDB
from .factory import RedisFactory

class Field:
  def __init__(self, field_id: str, info: Dict[str, Any]):
    self.__id: str = field_id
    self.__info: Dict[str, Any] = info

  @property
  def info(self) -> Dict[str, Any]:
    return self.__info

  @property
  def id(self) -> str:
    return self.__id

class RedisModel(ObserverDB):
  redis = RedisFactory()

  def __init__(self, key: str):
    self.__key = key

  def get_fields(self) -> Dict[str, Field]:
    elems_serialized: Dict[str, str] = RedisModel.redis.hgetall(self.__key)
    elems_deserialized: Dict[str, Field] =\
         {key: Field(key, json.loads(val))
         for key, val in elems_serialized.items()}
    return elems_deserialized

  def save(self, fields: List[Field]) -> None:
    if len(fields) > 0:
      dict_field: Dict[str, Field] = {field.id: json.dumps(field.info) for field in fields}
      RedisModel.redis.expire(self.__key)
      RedisModel.redis.hmset(self.__key, mapping=dict_field)
      super().save()
    else:
      print('empty fields try to be save into redis')#TODO log

  @staticmethod
  def del_keys_by_pattern(pattern: str) -> None:
    for key in RedisModel.redis.scan_iter(pattern+":*"):
      RedisModel.redis.delete(key)
