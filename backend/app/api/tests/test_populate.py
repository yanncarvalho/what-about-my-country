from unittest.mock import Mock, patch
from django.test import SimpleTestCase

from app.api.populate import Populate

class PopulateDBTest(SimpleTestCase):

  def setUp(self):
    self.Populate = Populate

  @patch('app.api.models_country.Country.save_from_net')
  @patch('app.api.models_country.Country.all_keys_n_name_from_net', return_value=[])
  def test_if_start_countries_then_calls_country_save_from_net(self, country_save_from_net, _):
    self.Populate.start_countries()
    country_save_from_net.assert_called()

  @patch('app.api.populate.Populate._is_populating', False)
  def test_if_run_n_is_populating_False_then_calls_start_populations(self):
   populate = self.Populate()
   populate.start_populations = Mock()  # override start_populations method
   populate.run()
   populate.start_populations.assert_called()

  @patch('app.api.populate.Populate._is_populating', True)
  def test_if_run_n_is_populating_True_then_not_calls_start_populations(self):
   populate = self.Populate()
   populate.start_populations = Mock()  # override start_populations method
   populate.run()
   populate.start_populations.assert_not_called()
