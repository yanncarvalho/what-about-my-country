from backend.api import helpers, models
from django.conf import settings as conf

class Country(models.RedisModel):

  _REDIS_COUNTRIES_ID: str = 'iso2code'

  def __init__(self, country_code: str):
    key = Country._REDIS_COUNTRIES_ID + ':' + country_code.upper()
    self.__fields: dict = {}
    self.__has_field_set: bool = False
    super().__init__(key=key)

  def __str__(self) -> str:
    return f'{self.__fields}'

  def __repr__(self) -> str:
    return f'{self.__fields}'

  def get_fields(self) -> dict:
    if self.__has_field_set is False:
       self.__field = super().get_fields()
    return self.__fields


  def set_fields(self, fields: list):
    self.__has_field_set = True
    self.__fields = fields


  def get_field(self, field_id: str):
    if self.__has_field_set is False:
       self.__field = super().get_field(field_id)
    return self.__field


  def add_field(self, field: models.Field):
    self.__has_field_set = True
    self.__fields += field

  def save(self) -> None:
    return super().save(self.fields)

  @classmethod
  def get_from_internet(cls, country_code):
    from_net = helpers.get_from_net(country_code)
    from_net_fields = [models.Field(k, v)
                       for k, v in from_net[country_code].items()]
    country = cls(country_code)
    country.set_fields(from_net_fields)
    return country

  @classmethod
  def all_countries_from_net(cls) -> list:
    countries = helpers.get_from_net()
    result: list = []
    for key in countries.keys():
      country =cls(key)
      fields = [models.Field(k, v)
                for k, v in countries[key].items()]
      country.set_fields(fields)
      result.append(country)
    return result

  @staticmethod
  def all_keys() -> list:
    return models.RedisModel.all_keys(Country._REDIS_COUNTRIES_ID)

  @staticmethod
  def all_fields_keys() -> set:
    return set(conf.FROM_NET_KEY_TO_FIELD_VALUE.values()).union(
        {conf.BASIC_INFO_FIELD})