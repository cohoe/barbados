import redis


class RedisConnector:
    def __init__(self, host='localhost', port=6379):
        self.host = host
        self.port = port

        self.client = redis.Redis(host=host, port=port, db=0)

    def set(self, key, value):
        return self.client.set(name=key, value=value)

    def get(self, key):
        value = self.client.get(name=key)

        if not value:
            raise KeyError

        return value
