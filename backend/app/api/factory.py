
from typing import Union

from django.conf import settings as conf
from redis import Redis

import logging

class RedisFactory(Redis):

  def __init__(self):
    """initialize redis db"""
    redis_conf = conf.REDIS

    super().__init__(
                  db=redis_conf['db'],
                  host=redis_conf['host'],
                  port=redis_conf['port'],
                  charset=redis_conf['charset'],
                  decode_responses=redis_conf['decode_responses'],
                  username=redis_conf['username'],
                  password=redis_conf['password'])
    #create time expire key
    conv_days_to_sec: int = lambda days: days * 24 * 60 * 60
    expire_in_days: int = redis_conf['expire_key_in_days']
    self.__redis_expire_in_secs: int = conv_days_to_sec(expire_in_days)



  def expire(self,
             name: Union[bytes, str, memoryview],
             nx: bool = False,
             xx: bool = False,
             gt: bool = False,
             lt: bool = False,) -> bool:
    """
    Set an expire flag on key ``name`` for default ``time`` define in ``settings.py``.

    Valid options are:
        - NX -> Set expiry only when the key has no expiry
        - XX -> Set expiry only when the key has an existing expiry
        - GT -> Set expiry only when the new expiry is greater than current one
        - LT -> Set expiry only when the new expiry is less than current one

    For more information see https://redis.io/commands/expire
    """
    logging.info(
        f'it has been set timeout {self.__redis_expire_in_secs} to key {name}')
    return super().expire(name = name,
                          time = self.__redis_expire_in_secs,
                          nx = nx,
                          xx = xx,
                          gt = gt,
                          lt = lt)
  @classmethod
  def redis_connected_or_exception(cls):
    """ verify if redis is connected
    Raises:
      RuntimeError: if it is not possible to connect to redis
    """
    try:
      cls().ping()
    except Exception as error:
        logging.critical('redis is not connecting')
        raise RuntimeError('redis is not connecting') from error
