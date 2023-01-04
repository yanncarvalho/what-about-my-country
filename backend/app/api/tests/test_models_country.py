"""Country test"""

import asyncio
from unittest.mock import AsyncMock, patch
from django.test import SimpleTestCase
from app.api import helpers, models_country

# pylint: disable=C0116, C0103, W0212, C0301
class CountryTest(SimpleTestCase):
    """Country test class"""

    def setUp(self):
        self.key = 'IND'  # some country iso2Code
        self.Country = models_country.Country

    @patch('app.api.models.RedisModel.save')
    def test_if_save_from_net_then_calls_redismodel_save_n_helpers_get_from_net(self, redis_save):
        mock_get_from_net = AsyncMock()

        async def override_get_from_net(key):
            await mock_get_from_net(key)
            return {}
        helpers.get_from_net = override_get_from_net
        asyncio.run(self.Country.save_from_net(self.key))
        redis_save.assert_called()
        mock_get_from_net.assert_awaited()

    @patch('app.api.models.RedisModel.get_fields')
    def test_if_get_fields_then_calls_redismodel_get_fields(self, redis_get_fields):
        self.Country(self.key).get_fields()
        redis_get_fields.assert_called()

    @patch('app.api.helpers.get_keys_n_name_from_net')
    def test_if_all_keys_from_net_then_calls_helpers_get_keys_from_net(
                    self, helpers_get_keys_n_name_from_net):
        self.Country.all_keys_n_name_from_net()
        helpers_get_keys_n_name_from_net.assert_called()

    @patch('app.api.models.RedisModel.get_fields', return_value=[])
    def test_if_is_empty_returns_True(self, _):
        is_empty = self.Country(self.key).is_empty()
        self.assertTrue(is_empty)

    @patch('app.api.models.RedisModel.get_fields', return_value=['ANY VALUE'])
    def test_if_is_not_empty_returns_False(self, _):
        is_empty = self.Country(self.key).is_empty()
        self.assertFalse(is_empty)

    @patch('app.api.models.RedisModel.del_keys_by_pattern')
    def test_if_del_all_countries_then_calls_redismodel_del_keys_by_pattern(
            self, redis_del_keys_by_pattern):
        self.Country.del_all_countries()
        redis_del_keys_by_pattern.assert_called()

    @patch('app.api.models_country.Country.save_from_net')
    @patch('app.api.models_country.Country._is_populating', False)
    @patch('app.api.models_country.Country.all_keys_n_name_from_net', return_value=[])
    def test_if_save_all_countries_n_is_populating_False_then_save_from_net(self, country_save_from_net, _):
        self.Country.save_all_countries()
        country_save_from_net.assert_called()

    @patch('app.api.models_country.Country.save_from_net')
    @patch('app.api.models_country.Country._is_populating', True)
    @patch('app.api.models_country.Country.all_keys_n_name_from_net', return_value=[])
    def test_if_save_all_countries_n_is_populating_True_then_not_call_start_populations(self, country_save_from_net, _):
        self.Country.save_all_countries()
        country_save_from_net.start_populations.assert_not_called()
