import asyncio
from typing import Optional, Set
from django.test import SimpleTestCase
from app.api import helpers

class HelpersTest(SimpleTestCase):

  def setUp(self):
   async def override_get_items_wbank_api(*_):
        return [{
            'id': 'Test',
            'name': 'Test',
            'region': {'value': 'test'},
            'capitalCity': 'Test',
            'longitude': 0,
            'latitude': 0,
            'incomeLevel': {'value': 'test'}
        }]

   async def override_get_items_wbank_api_return_None(*_):
       return None
   self.override_get_items_wbank_api = override_get_items_wbank_api
   self.override_get_items_wbank_api_return_None = override_get_items_wbank_api_return_None


  def test_if_get_keys_from_net_then_success(self):
   helpers._get_items_wbank_api = self.override_get_items_wbank_api
   keys: Set[str] = helpers.get_keys_from_net()
   self.assertIsInstance(keys, set, 'keys is not a set')
   self.assertNotEqual(len(keys), 0, 'keys is empty')
   for key in keys:
    self.assertIsInstance(key, str, f'{key} is not a String')

  def test_if_get_from_net_then_success(self):
    key: str = 'Test' #any country
    helpers._get_items_wbank_api = self.override_get_items_wbank_api
    country: Optional[helpers.CountryAPIRequest] = asyncio.run(
        helpers.get_from_net(key))

    self.assertIsInstance(country, dict, 'country is not a dictionary')
    self.assertNotEqual(len(country), 0,  'country is empty')

    for key, value in country.items():
        self.assertIs(type(key), str, f'key {key} must be an String')
        self.assertIs(type(value), dict, f'value {value} must be a dictionary')

  def test_if_get_from_net_with_empty_key_then_exception(self):
    key: str = ''  # none
    with self.assertRaises(ValueError):
      asyncio.run(helpers.get_from_net(key))

  def test_if_get_from_net_with_invalid_key_then_exception(self):
    key: int = 1  # wrong type
    with self.assertRaises(ValueError):
      asyncio.run(helpers.get_from_net(key))

  def test_if_get_from_net_with_non_exist_key_then_empty_dict(self):
    helpers._get_items_wbank_api = self.override_get_items_wbank_api_return_None
    key: str = 'INVALID'
    country: Optional[helpers.CountryAPIRequest] = asyncio.run(helpers.get_from_net(key))
    self.assertIs(country, None, 'country is not None')