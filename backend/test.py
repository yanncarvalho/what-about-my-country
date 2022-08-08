from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from backend.populate import Populate

class PopulateDBTest(SimpleTestCase):

  def setUp(self):
    self.Populate = Populate

  @patch('backend.api.models_country.Country.save_from_net')
  def test_if_start_countries_then_calls_country_save_from_net(self, country_save_from_net):
    self.Populate.start_countries()
    country_save_from_net.assert_called()

  @patch('backend.populate.Populate._is_population', False)
  def test_if_run_n_is_population_False_then_calls_start_populations(self):
   populate = self.Populate()
   populate.start_populations = Mock()  # override start_populations method
   populate.run()
   populate.start_populations.assert_called()

  @patch('backend.populate.Populate._is_population', True)
  def test_if_run_n_is_population_True_then_not_calls_start_populations(self):
   populate = self.Populate()
   populate.start_populations = Mock()  # override start_populations method
   populate.run()
   populate.start_populations.assert_not_called()