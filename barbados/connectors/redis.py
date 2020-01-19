import redis
import barbados.config


class RedisConnector:
    def __init__(self):
        self.host = barbados.config.cache.redis_host
        self.port = barbados.config.cache.redis_port
        self.username = barbados.config.cache.redis_username  # this isn't here yet
        self.password = barbados.config.cache.redis_password
        self.ssl = barbados.config.cache.redis_ssl

        self.client = redis.Redis(host=self.host, port=self.port, password=self.password, ssl=self.ssl, db=0)

    def set(self, key, value):
        return self.client.set(name=key, value=value)

    def get(self, key):
        value = self.client.get(name=key)

        if not value:
            raise KeyError

        return value
