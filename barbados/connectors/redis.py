import os
from barbados.exceptions import ServiceUnavailableException
from redis import Redis, exceptions
from barbados.services.logging import LogService
from barbados.settings import Setting


class RedisConnector:
    """
    Connector to the Redis cache service. The CacheService creates an instance of this connector
    and uses it to communicate with the backend.
    @TODO implement global connection pooling somewhere
    """
    def __init__(self):
        self.host = Setting(path='/cache/redis/host', env='AMARI_REDIS_HOST', default='127.0.0.1', type_=str).get_value()
        self.port = Setting(path='/cache/redis/port', env='AMARI_REDIS_PORT', default=6379, type_=int).get_value()
        self.username = Setting(path='/cache/redis/username', env='AMARI_REDIS_USERNAME', default=None, type_=str).get_value()
        self.password = Setting(path='/cache/redis/password', env='AMARI_REDIS_PASSWORD', default=None, type_=str).get_value()
        self.ssl = Setting(path='/cache/redis/ssl', env='AMARI_REDIS_SSL', default=False, type_=bool).get_value()

        LogService.info("Redis connection: %s:%s@%s:%s?ssl=%s" % (self.username, self.password, self.host, self.port, self.ssl))

    def set(self, key, value):
        self._connect()
        return self.client.set(name=key, value=value)

    def get(self, key):
        try:
            self._connect()
            value = self.client.get(name=key)
        except exceptions.ConnectionError as e:
            raise ServiceUnavailableException("Cache error: %s" % str(e))

        if not value:
            raise KeyError

        return value

    def delete(self, key):
        self._connect()
        self.client.delete(key)

    def _connect(self):
        if not hasattr(self, 'client'):
            self.client = Redis(host=self.host, port=self.port, password=self.password, ssl=self.ssl, db=0)

        return
