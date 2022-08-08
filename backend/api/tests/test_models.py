from unittest.mock import  Mock, patch
from django.test import SimpleTestCase
from backend.api import models, factory

class RedisModelTest(SimpleTestCase):

  def mock_class_methods(self, cls):
    method_list = dir(cls)
    for method in method_list:
      if method.startswith('_') is False:
        setattr(cls, method, Mock())
    return cls

  def setUp(self):
    self.RedisModel = models.RedisModel
    self.key = 'ANY_THING'
    self.mock_redis = self.mock_class_methods(factory.RedisFactory)

  def test_if_del_keys_by_pattern_then_calls_redis_delete(self):
    def override_scan_iter(*args, **kwargs):
      return [self.key]

    self.mock_redis.scan_iter = override_scan_iter
    self.RedisModel.del_keys_by_pattern(self.key)
    self.mock_redis.delete.assert_called()

  def test_if_save_then_calls_redis_expire(self):
    fake_fields = [models.Field('ANY', {})]
    self.RedisModel(self.key).save(fake_fields)
    self.mock_redis.expire.assert_called()

  def test_if_save_then_calls_redis_hmset(self):
    fake_fields = [models.Field('ANY', {})]
    self.RedisModel(self.key).save(fake_fields)
    self.mock_redis.hmset.assert_called()

  def test_if_save_with_empty_fields_then_not_calls_redis_hmset(self):
    fake_empty_fields = []
    self.RedisModel(self.key).save(fake_empty_fields)
    self.mock_redis.hmset.assert_not_called()

  def test_if_save_with_empty_fields_then_not_calls_redis_expire(self):
    fake_empty_fields = []
    self.RedisModel(self.key).save(fake_empty_fields)
    self.mock_redis.expire.assert_not_called()

  @patch('backend.api.observer.ObserverDB.save')
  def test_if_save_then_calls_observer_save(self, observerdb_save):
    fake_fields = [models.Field('ANY', {})]
    self.RedisModel(self.key).save(fake_fields)
    observerdb_save.assert_called()
