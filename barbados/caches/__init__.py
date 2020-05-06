import json
import pickle
from barbados.models import IngredientModel, CocktailModel
from barbados.services import Cache, Registry
from barbados.services.logging import Log
from barbados.objects.ingredienttree import IngredientTree
from barbados.serializers import ObjectSerializer
from barbados.factories import CocktailFactory, IngredientFactory


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
            Log.warning("Attempted to retrieve '%s' but it was empty. Repopulating..." % cls.cache_key)
            cls.populate()
            return pickle.loads(Cache.get(cls.cache_key))
