import json
import pickle
import logging
from barbados.models import IngredientModel, CocktailModel
from barbados.services import Cache, Registry
from barbados.objects.ingredienttree import IngredientTree
from barbados.serializers import ObjectSerializer
from barbados.factories import CocktailFactory, IngredientFactory


class Caches:
    """
    Holder for all data caches. This enables simple lookup by cache_key
    such as Caches('ingredient_name_index').
    """
    caches = {}

    # Apparently __call__() didn't work?
    # https://stackoverflow.com/questions/34777773/typeerror-object-takes-no-parameters-after-defining-new
    def __new__(cls, cache_key):
        """
        Act kinda like an enum in that this will return the class for a given
        cache key
        :param cache_key: String of the cache key.
        :return class or KeyError.
        """
        return cls.caches[cache_key]

    @classmethod
    def register_cache(cls, cache_class):
        """
        Register a cache class for use and lookup by this class.
        :param cache_class: Class (the class, not a string) to register
        :return: None
        """
        cls.caches[cache_class.cache_key] = cache_class


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
            logging.warning("Attempted to retrieve '%s' but it was empty. Repopulating..." % cls.cache_key)
            cls.populate()
            return Cache.get(cls.cache_key)

    @classmethod
    def invalidate(cls):
        """
        Invalidate (delete) the cache value and key.
        :return: None
        """
        logging.info("Invalidating cache key %s" % cls.cache_key)
        return Cache.delete(cls.cache_key)

    @property
    def cache_key(self):
        raise NotImplementedError


class UsableIngredientCache(CacheBase):
    cache_key = 'ingredient_name_index'

    @classmethod
    def populate(cls, **kwargs):
        # This is still returning all values, just not populating them
        pgconn = Registry.get_database_connection()

        index = []
        with pgconn.get_session() as session:
            scan_results = IngredientModel.get_usable_ingredients(session)

            for result in scan_results:
                index.append({
                    'slug': result.slug,
                    'display_name': result.display_name,
                    'aliases': result.aliases,
                })

        Cache.set(cls.cache_key, json.dumps(index))


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
        # This is still returning all values, just not populating them
        pgconn = Registry.get_database_connection()
        cache_objects = []
        with pgconn.get_session() as session:
            results = session.query(cls.model_class).all()
            for result in results:
                result_object = cls.factory_class.model_to_obj(model=result)
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
            logging.warning("Attempted to retrieve '%s' but it was empty. Repopulating..." % cls.cache_key)
            cls.populate()
            return pickle.loads(Cache.get(cls.cache_key))


Caches.register_cache(UsableIngredientCache)
Caches.register_cache(CocktailScanCache)
Caches.register_cache(IngredientTreeCache)
Caches.register_cache(IngredientScanCache)
