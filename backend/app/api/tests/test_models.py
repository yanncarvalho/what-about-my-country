"""Redis Model test"""

from unittest.mock import Mock
from django.test import SimpleTestCase
from app.api import models, factory

# pylint: disable=C0116, C0103, W0212, E1101, W0613
class RedisModelTest(SimpleTestCase):
    """Redis Model test class"""
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
        self.mock_redis.expire = Mock()
        self.RedisModel(self.key).save(fake_empty_fields)
        self.mock_redis.hmset.assert_not_called()

    def test_if_save_with_empty_fields_then_not_calls_redis_expire(self):
        fake_empty_fields = []
        self.mock_redis.expire = Mock()
        self.RedisModel(self.key).save(fake_empty_fields)
        self.mock_redis.expire.assert_not_called()
