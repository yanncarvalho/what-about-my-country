import statistics
from backend.api import models

class Country(models.RedisModel):

  _REDIS_COUNTRY_ID: str = 'iso2code'+':'

  def __init__(self, country_code: str):
    super().__init__(key=country_code, id_reference=Country._REDIS_COUNTRY_ID)

  @staticmethod
  def all_keys() -> list:
    return models.RedisModel.all_keys(Country._REDIS_COUNTRY_ID)
