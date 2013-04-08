'''
Created on 6.4.2013

@author: Martin Babka
'''
from asl.cache.cache_module import CacheModule
import redis
from asl.application.service_application import service_application

class RedisCacheModule(CacheModule):
    '''
    Abstraction layer for caching.
    '''
    def __init__(self):
        '''
        Abstraction layer for caching.
        '''
        self._app = service_application
        redis_conf = self._app.config['REDIS'];
        self._client = redis.StrictRedis(
            host=redis_conf['host'],
            port = redis_conf['port'],
            db = redis_conf['db'],
            password = redis_conf['password']
        )
        self._app.logger.debug("Redis client created.")

    def set_key(self, key, value, timeout):
        self._client.set(key, value)
        self._client.expire(key, timeout)

    def invalidate_key(self, key):
        self._client.delete(key)

    def contains_key(self, key):
        return self._client.exists(key)

    def get_key(self, key):
        return self._client.get(key)

    def append_to_list(self, key, value):
        self._client.rpush(key, value)

    def get_list(self, key):
        llen = self._client.llen(key)
        return self._client.getrange(key, 0, llen - 1)
