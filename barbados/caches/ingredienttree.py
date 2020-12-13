import pickle
from barbados.caches import Caches
from barbados.caches.base import CacheBase
from barbados.services.cache import Cache
from barbados.services.logging import Log
from barbados.objects.ingredienttree import IngredientTree


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


Caches.register_cache(IngredientTreeCache)
