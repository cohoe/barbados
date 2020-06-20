import os
from barbados.exceptions import ServiceUnavailableException
from redis import Redis, exceptions
from barbados.services.logging import Log


# @TODO implement global connection pooling somewhere


class RedisConnector:
    def __init__(self, host=os.getenv('REDIS_HOST', default='127.0.0.1'),
                 port=int(os.getenv('REDIS_PORT', default=6379)),
                 username=None, password=None, ssl=False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ssl = ssl

        Log.info("Using Redis host: \"%s:%i\"" % (host, port))

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
