
from unittest.mock import patch

from app.api.observer import ObserverDB
from django.test import SimpleTestCase


class ObserverDBTest(SimpleTestCase):

  def setUp(self):
    self.ObserverDB = ObserverDB

  @patch('app.api.populate.Populate.start')
  def test_if_save_then_calls_populate_start(self, populate_start):
    self.ObserverDB().save()
    populate_start.assert_called()


