
from unittest.mock import patch

from backend.api.observer import ObserverDB
from django.test import SimpleTestCase


class ObserverDBTest(SimpleTestCase):

  def setUp(self):
    self.ObserverDB = ObserverDB

  @patch('backend.api.populate.Populate.start')
  def test_if_save_then_calls_populate_start(self, populate_start):
    self.ObserverDB().save()
    populate_start.assert_called()


