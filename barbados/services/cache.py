from barbados.connectors.redis import RedisConnector


class CacheService:
    """
    Generic cache class. This exists to provide a common interface
    to the connectors. Potential connectors could be:
    * Redis
    * Memcached
    """

    connector = RedisConnector()

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
