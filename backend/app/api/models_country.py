from typing import Dict, List, Set, Optional
from app.api import helpers, models

class Country:
  """Country class represeting database data and World Bank API."""

  _REDIS_COUNTRIES_ID: str = 'api:country:iso3code'

  def __init__(self, country_code: str):
    """Inits Country with country iso3code id."""
    key: str = ':'.join((Country._REDIS_COUNTRIES_ID, country_code.upper()))
    Country._database = models.RedisModel(key=key)

  def get_fields(self) -> Dict[str ,models.Field]:
    """get information from the database"""
    return Country._database.get_fields()

  def is_empty(self) -> bool:
    """check if a country in the database has fields"""
    return not bool(Country._database.get_fields())

  @classmethod
  async def save_from_net(cls, country_code: str) -> None:
    """save a country with its iso3code id from World Bank API in the database."""
    from_net: Optional[helpers.CountryAPIRequest] = await helpers.get_from_net(country_code)
    from_net_fields: List[models.Field] = \
      [models.Field(k, v) for k, v in from_net.items()]
    cls(country_code)._database.save(from_net_fields)

  @staticmethod
  def all_keys_from_net() -> Set[str]:
    """get country iso3code id from World Bank API"""
    return helpers.get_keys_from_net()

  @staticmethod
  def del_all_countries() -> None:
    """delete all countries from the database"""
    models.RedisModel.del_keys_by_pattern(Country._REDIS_COUNTRIES_ID)