from redis import Redis
from barbados.services.logging import Log

# @TODO implement global connection pooling somewhere


class RedisConnector:
    def __init__(self, host='127.0.0.1', port=6379, username=None, password=None, ssl=False):
        self.host = host
        self.port = port
        # Log.info("Using Redis host: \"%s%i\"" % (host, port))
        self.username = username
        self.password = password
        self.ssl = ssl

    def set(self, key, value):
        self._connect()
        return self.client.set(name=key, value=value)

    def get(self, key):
        self._connect()
        value = self.client.get(name=key)

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
