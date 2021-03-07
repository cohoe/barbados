from barbados.connectors.redis import RedisConnector
from barbados.settings.cache import redis_settings


class CacheService:
    """
    Generic cache class. This exists to provide a common interface
    to the connectors. Potential connectors could be:
    * Redis
    * Memcached
    """

    connector = RedisConnector(**redis_settings)

    @staticmethod
    def get(key):
        """
        Fetch the value from the cache for the given key.
        :param key: Cache key.
        :return: str or Exception
        """
        return CacheService.connector.get(key)

    @staticmethod
    def set(key, value):
        """
        Set a given key in the cache to a value. This
        will create the key if it does not exist.
        :param key: Cache key.
        :param value: String of the value to set
        :return: None or Exception
        """
        return CacheService.connector.set(key, value)

    @staticmethod
    def delete(key):
        """
        Delete a given key.
        :param key: cache key
        :return: None or Exception
        """
        return CacheService.connector.delete(key)

    @staticmethod
    def get_flask_config():
        """
        Return a dictionary of Flask_Caching config directives.
        https://flask-caching.readthedocs.io/en/latest/#configuring-flask-caching
        :return: Dict
        """
        return {
            'CACHE_TYPE': 'redis',
            'CACHE_REDIS_HOST': CacheService.connector.host,
            'CACHE_REDIS_PORT': CacheService.connector.port,
            'CACHE_REDIS_DB': CacheService.connector.flask_database_id,
            'CACHE_DEFAULT_TIMEOUT': CacheService.connector.request_timeout,
        }
