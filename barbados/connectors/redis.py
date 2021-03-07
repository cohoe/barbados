from barbados.exceptions import ServiceUnavailableException
from redis import Redis, exceptions
from barbados.services.logging import LogService


class RedisConnector:
    """
    Connector to the Redis cache service. The CacheService creates an instance of this connector
    and uses it to communicate with the backend.
    """
    def __init__(self, host, port, username, password, ssl, request_timeout, flask_database_id):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ssl = ssl
        self.request_timeout = request_timeout
        self.flask_database_id = flask_database_id
        LogService.info("Redis connection: redis://%s:%s@%s:%s?ssl=%s" % (self.username, self.password, self.host, self.port, self.ssl))

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
