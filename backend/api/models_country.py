from backend.api import helpers, models
from django.conf import settings as conf


class Country(models.RedisModel):

  _REDIS_COUNTRIES_ID: str = 'api:country:iso2code'

  def __init__(self, country_code: str):
    self.__code = country_code
    key = Country._REDIS_COUNTRIES_ID + ':' + country_code.upper()
    self.__fields: dict = {}
    self.__has_field_set: bool = False
    super().__init__(key=key)

  @property
  def code(self) -> dict:
    return self.__code

  def __str__(self) -> str:
    return f'{self.__fields}'

  def __repr__(self) -> str:
    return f'{self.__fields}'

  def get_fields(self) -> dict:
    if self.__has_field_set is False:
       self.__fields = super().get_fields()
    return self.__fields

  def set_fields(self, fields: list):
    self.__has_field_set = True
    self.__fields = fields

  def get_field(self, field_id: str):
    field = None
    if self.__has_field_set is False:
       field = super().get_field(field_id)
    return field


  def add_field(self, field: models.Field):
    self.__has_field_set = True
    self.__fields += field

  def save(self) -> None:
    return super().save(self.__fields)

  def set_fields_from_internet(self) -> None:
    from_net = helpers.get_from_net(self.__code)
    from_net_fields = [models.Field(k, v)
                       for k, v in from_net[self.__code].items()]
    self.set_fields(from_net_fields)

  def is_empty(self) -> bool:
    return not bool(self.get_fields())

  @staticmethod
  def all_keys_from_internet() -> set:
    return helpers.get_keys_from_net()

  @staticmethod
  def all_keys() -> list:
    return models.RedisModel.all_keys(Country._REDIS_COUNTRIES_ID)

  @staticmethod
  def del_all_countries() -> None:
    models.RedisModel.del_keys_by_pattern(Country._REDIS_COUNTRIES_ID)

  @staticmethod
  def all_fields_keys() -> set:
    return set(conf.FROM_NET_KEY_TO_FIELD_VALUE.values()).union(
        {conf.BASIC_INFO_FIELD})

