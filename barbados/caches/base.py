from barbados.services.cache import CacheService
from barbados.services.logging import LogService


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
            return CacheService.get(cls.cache_key)
        except KeyError:
            LogService.warning("Attempted to retrieve '%s' but it was empty. Repopulating..." % cls.cache_key)
            cls.populate()
            return CacheService.get(cls.cache_key)

    @classmethod
    def invalidate(cls):
        """
        Invalidate (delete) the cache value and key.
        :return: None
        """
        LogService.info("Invalidating cache key %s" % cls.cache_key)
        return CacheService.delete(cls.cache_key)

    @property
    def cache_key(self):
        raise NotImplementedError()
