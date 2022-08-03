from typing import Dict, List, Set
from backend.api import helpers, models


class Country:

  _REDIS_COUNTRIES_ID: str = 'api:country:iso3code'

  def __init__(self, country_code: str):
    key: str = ':'.join((Country._REDIS_COUNTRIES_ID, country_code.upper()))
    Country._database = models.RedisModel(key=key)

  def get_fields(self) -> Dict[str ,models.Field]:
    return Country._database.get_fields()

  def is_empty(self) -> bool:
    return not bool(Country._database.get_fields())

  @classmethod
  async def save_from_net(cls, country_code: str) -> None:
    from_net: Dict[str, Dict[str, object]] = await helpers.get_from_net(country_code)
    from_net_fields: List[models.Field] = \
      [models.Field(k, v) for k, v in from_net.items()]
    cls(country_code)._database.save(from_net_fields)

  @staticmethod
  def all_keys_from_net() -> Set[str]:
    return helpers.get_keys_from_net()

  @staticmethod
  def del_all_countries() -> None:
    models.RedisModel.del_keys_by_pattern(Country._REDIS_COUNTRIES_ID)