"""Model classes"""
import json
from typing import Any, Dict, List
import logging
from .factory import RedisFactory


class Field:
    """Field class represeting the database field.

    Attributes:
      id: database id
      info: dictionary with field information
    """
    def __init__(self, field_id: str, info: Dict[str, Any]):
        """Inits Field with field_id and info"""
        self.__id: str = field_id
        self.__info: Dict[str, Any] = info

    @property
    def info(self) -> Dict[str, Any]:
        """dictionary with field information"""
        return self.__info

    # pylint: disable=invalid-name
    @property
    def id(self) -> str:
        """database id"""
        return self.__id

class RedisModel:
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
            dict_field: Dict[str, Field] = {
                field.id: json.dumps(field.info) for field in fields}
            RedisModel.redis.expire(self.__key)
            logging.info(
                'saving new information in redis, with key %s', self.__key)
            RedisModel.redis.hmset(self.__key, mapping=dict_field)
        else:
            logging.error('empty fields try to be save in redis')

    @staticmethod
    def del_keys_by_pattern(pattern: str) -> None:
        """delete information from the database that match the specific pattern"""
        for key in RedisModel.redis.scan_iter(pattern+":*"):
            logging.info('delete information from redis with key %s', key)
            RedisModel.redis.delete(key)
