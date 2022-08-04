import json
from typing import Any, Dict, List

from .observer import ObserverDB
from .factory import RedisFactory

class Field:
  """Field class represeting the database field.

  Attributes:
    field_id: database id
    info: dictionary with field information
  """
  def __init__(self, field_id: str, info: Dict[str, Any]):
    """Inits Field with field_id and info"""
    self.__id: str = field_id
    self.__info: Dict[str, Any] = info

  @property
  def info(self) -> Dict[str, Any]:
    return self.__info

  @property
  def id(self) -> str:
    return self.__id

class RedisModel(ObserverDB):
  """RedisModel class represeting Redis used as database"""

  redis = RedisFactory()

  def __init__(self, key: str):
    """Inits RedisModel with key ID for requesting information from the database"""
    self.__key = key

  def get_fields(self) -> Dict[str, Field]:
    """get fields from database"""
    elems_serialized: Dict[str, str] = RedisModel.redis.hgetall(self.__key)
    elems_deserialized: Dict[str, Field] =\
         {key: Field(key, json.loads(val))
         for key, val in elems_serialized.items()}
    return elems_deserialized

  def save(self, fields: List[Field]) -> None:
    """save fields in database"""
    if len(fields) > 0:
      dict_field: Dict[str, Field] = {field.id: json.dumps(field.info) for field in fields}
      RedisModel.redis.expire(self.__key)
      RedisModel.redis.hmset(self.__key, mapping=dict_field)
      super().save()
    else:
      print('empty fields try to be save into redis')#TODO log

  @staticmethod
  def del_keys_by_pattern(pattern: str) -> None:
    """delete information from the database that match the specific pattern"""
    for key in RedisModel.redis.scan_iter(pattern+":*"):
      RedisModel.redis.delete(key)
