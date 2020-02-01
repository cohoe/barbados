import redis

# @TODO implement global connection pooling somewhere


class RedisConnector:
    def __init__(self, host='127.0.0.1', port=6379, username=None, password=None, ssl=False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ssl = ssl

        self.client = redis.Redis(host=self.host, port=self.port, password=self.password, ssl=self.ssl, db=0)

    def set(self, key, value):
        return self.client.set(name=key, value=value)

    def get(self, key):
        value = self.client.get(name=key)

        if not value:
            raise KeyError

        return value

    def delete(self, key):
        self.client.delete(key)
