class CacheFactory:
    """
    Producer and manager of all cache objects.
    """
    def __init__(self):
        self._keys = {}

    def register_cache(self, cache):
        """
        Register a cache with the system. This makes it findable
        by various methods by key, and maintains a list of all caches.
        :param cache: barbados.caches.base.CacheBase child class.
        :return: None
        """
        self._keys[cache.cache_key] = cache

    def cache_keys(self):
        """
        Return a list of a all cache keys registered.
        :return: List(String)
        """
        return list(self._keys.keys())

    def get_cache(self, key):
        """
        Return the Cache class matching a particular key.
        :param key: string of the redis cache key.
        :raises KeyError: The key was not found.
        :return: CacheBase child object.
        """
        cache = self._keys.get(key)
        if cache is None:
            raise KeyError("Cache '%s' not found." % key)
        return cache


# This is the thing that you import in other caches and use to register
# that cache with the system. Also used if you want to retrieve a cache
# that you only know the key for.
Caches = CacheFactory()
