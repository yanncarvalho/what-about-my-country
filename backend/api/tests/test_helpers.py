import asyncio
from typing import Dict, Set
from django.test import SimpleTestCase
from backend.api import helpers

class HelpersTest(SimpleTestCase):

  def test_if_get_keys_from_net_then_success(self):
    keys: Set[str] = helpers.get_keys_from_net()
    self.assertIsInstance(keys, set, 'keys is not a set')
    self.assertNotEqual(len(keys), 0, 'keys is empty')
    for key in keys:
      self.assertIsInstance(key, str, f'{key} is not a String')

  def test_if_get_from_net_then_success(self):
    key: str = 'CYP'
    country: Dict[str, Dict[str, object]] = asyncio.run(helpers.get_from_net(key))
    self.assertIsInstance(country, dict, 'country is not a dictionary')
    self.assertNotEqual(len(country), 0,  'country is empty')

    for key, value in country.items():
        self.assertIs(type(key), str, f'key {key} must be an String')
        self.assertIs(type(value), dict, f'value {value} must be a dictionary')

  def test_if_get_from_net_with_empty_key_then_exception(self):
    key: str = ''
    with self.assertRaises(ValueError):
      asyncio.run(helpers.get_from_net(key))

  def test_if_get_from_net_with_invalid_key_then_exception(self):
    key: int = 1
    with self.assertRaises(ValueError):
      asyncio.run(helpers.get_from_net(key))

  def test_if_get_from_net_with_non_exist_key_then_empty_dict(self):
    key: str = 'INVALID'
    country: Dict[str, Dict[str, object]] = asyncio.run(helpers.get_from_net(key))
    self.assertIsInstance(country, dict, 'keys is not a set')
    self.assertEqual(len(country), 0, 'keys is  not empty')
