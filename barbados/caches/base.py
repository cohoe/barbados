from barbados.services.cache import Cache
from barbados.services.logging import Log


class CacheBase:
    """
    Base Cache class. Implements basic functions.
    """

    @staticmethod
    def populate():
        """
        Code that populates the cache should go here. It could take in
        parameters if you want, but you have to implement it in the
        subclasses.
        :return:
        """
        raise NotImplementedError()

    @classmethod
    def retrieve(cls):
        """
        Retrieve the cache's value
        :return: Various
        """
        try:
            return Cache.get(cls.cache_key)
        except KeyError:
            Log.warning("Attempted to retrieve '%s' but it was empty. Repopulating..." % cls.cache_key)
            cls.populate()
            return Cache.get(cls.cache_key)

    @classmethod
    def invalidate(cls):
        """
        Invalidate (delete) the cache value and key.
        :return: None
        """
        Log.info("Invalidating cache key %s" % cls.cache_key)
        return Cache.delete(cls.cache_key)

    @property
    def cache_key(self):
        raise NotImplementedError()
