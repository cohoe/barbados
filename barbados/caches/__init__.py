import json
import pickle
from barbados.models import IngredientModel, CocktailModel, MenuModel, InventoryModel
from barbados.services.cache import Cache
from barbados.services.registry import Registry
from barbados.services.logging import Log
from barbados.objects.ingredienttree import IngredientTree
from barbados.objects.bibliography import Bibliography
from barbados.serializers import ObjectSerializer
from barbados.factories import CocktailFactory, IngredientFactory, MenuFactory, InventoryFactory


class CacheFactory:
    def __init__(self):
        self._keys = {}

    def register_cache(self, cache):
        self._keys[cache.cache_key] = cache

    def cache_keys(self):
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
        :param cls:
        :return:
        """
        raise NotImplementedError()

    @classmethod
    def retrieve(cls):
        """
        Retrieve the cache's value
        :return: Various
        """
        # return Cache.get(cls.cache_key)
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
        raise NotImplementedError


class TableScanCache(CacheBase):

    @property
    def cache_key(self):
        raise NotImplementedError

    @property
    def model_class(self):
        raise NotImplementedError

    @property
    def factory_class(self):
        raise NotImplementedError

    @classmethod
    def populate(cls):
        """
        Populate the cache with its expected value(s).
        :return: None
        """
        pgconn = Registry.get_database_connection()

        with pgconn.get_session() as session:
            cache_objects = []
            objects = cls.factory_class.produce_all_objs(session=session)
            for result_object in objects:
                cache_objects.append(ObjectSerializer.serialize(result_object, 'dict'))

        Cache.set(cls.cache_key, json.dumps(cache_objects))


class CocktailScanCache(TableScanCache):
    cache_key = 'cocktail_scan_cache'
    model_class = CocktailModel
    factory_class = CocktailFactory


class IngredientScanCache(TableScanCache):
    cache_key = 'ingredient_scan_cache'
    model_class = IngredientModel
    factory_class = IngredientFactory


class MenuScanCache(TableScanCache):
    cache_key = 'menu_scan_cache'
    model_class = MenuModel
    factory_class = MenuFactory


class InventoryScanCache(TableScanCache):
    cache_key = 'inventory_scan_cache'
    model_class = InventoryModel
    factory_class = InventoryFactory


class IngredientTreeCache(CacheBase):
    """
    Serializing and cacheing objects is dangerous. But the Treelib
    doesn't have support for loading from JSON yet (only saving to).
    """
    cache_key = 'ingredient_tree_object'

    @classmethod
    def populate(cls):
        Cache.set(cls.cache_key, pickle.dumps(IngredientTree()))

    @classmethod
    def retrieve(cls):
        try:
            return pickle.loads(Cache.get(cls.cache_key))
        except KeyError:
            Log.warning("Attempted to retrieve '%s' but it was empty. Repopulating..." % cls.cache_key)
            cls.populate()
            return pickle.loads(Cache.get(cls.cache_key))


class RecipeBibliographyCache(CacheBase):
    """
    Cache a list of all Citations.
    """
    cache_key = 'recipe_bibliography_cache'

    @classmethod
    def populate(cls):
        serialized_citations = [ObjectSerializer.serialize(citation, 'dict') for citation in Bibliography().citations]
        Cache.set(cls.cache_key, json.dumps(serialized_citations))


cache_factory = CacheFactory()
cache_factory.register_cache(CocktailScanCache)
cache_factory.register_cache(IngredientScanCache)
cache_factory.register_cache(MenuScanCache)
cache_factory.register_cache(IngredientTreeCache)
cache_factory.register_cache(RecipeBibliographyCache)
cache_factory.register_cache(InventoryScanCache)
