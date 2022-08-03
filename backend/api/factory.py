from typing import Union
from django.conf import settings as conf
from redis import Redis

class RedisFactory(Redis):
  def __init__(self):
    redis_conf = conf.REDIS
    super().__init__(
                  port=redis_conf['port'],
                  charset=redis_conf['charset'],
                  decode_responses=redis_conf['decode_responses'])

    conv_days_to_sec: int = lambda days: days * 24 * 60 * 60
    expire_in_days: int = redis_conf['expire_key_in_days']
    self.__redis_expire_in_secs: int = conv_days_to_sec(expire_in_days)

  def expire(self,
             name: Union[bytes, str, memoryview],
             nx: bool = False,
             xx: bool = False,
             gt: bool = False,
             lt: bool = False,) -> bool:
    return super().expire(name = name,
                          time = self.__redis_expire_in_secs,
                          nx = nx,
                          xx = xx,
                          gt = gt,
                          lt = lt)
  @classmethod
  def redis_connected_or_exception(cls):
    try:
      cls().ping()
    except Exception as error:
        raise RuntimeError('redis is not connecting') from error
