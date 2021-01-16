import pickle
from barbados.caches import Caches
from barbados.caches.base import CacheBase
from barbados.services.cache import CacheService
from barbados.services.logging import LogService
from barbados.objects.ingredienttree import IngredientTree


class IngredientTreeCache(CacheBase):
    """
    Serializing and cacheing objects is dangerous. But the Treelib
    doesn't have support for loading from JSON yet (only saving to).
    """
    cache_key = 'ingredient_tree_object'

    @classmethod
    def populate(cls):
        CacheService.set(cls.cache_key, pickle.dumps(IngredientTree()))

    @classmethod
    def retrieve(cls):
        try:
            return pickle.loads(CacheService.get(cls.cache_key))
        except KeyError:
            LogService.warning("Attempted to retrieve '%s' but it was empty. Repopulating..." % cls.cache_key)
            cls.populate()
            return pickle.loads(CacheService.get(cls.cache_key))


Caches.register_cache(IngredientTreeCache)
