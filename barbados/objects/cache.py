from barbados.connectors import RedisConnector


class Cache:
    """
    Generic cache class. This exists to provide a common interface
    to the connectors. Potential connectors could be:
    * Redis
    * Memcached
    """

    cache_connector = RedisConnector()

    @staticmethod
    def get(key):
        """
        Fetch the value from the cache for the given key.
        :param key: Cache key.
        :return: str or Exception
        """
        return Cache.cache_connector.get(key)

    @staticmethod
    def set(key, value):
        """
        Set a given key in the cache to a value. This
        will create the key if it does not exist.
        :param key: Cache key.
        :param value: String of the value to set
        :return: None or Exception
        """
        return Cache.cache_connector.set(key, value)
