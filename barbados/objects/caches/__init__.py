import json
from barbados.models import IngredientModel, CocktailModel
from barbados.services import Cache


class Caches(object):
    caches = {}

    # Apparently __call__() didn't work?
    # https://stackoverflow.com/questions/34777773/typeerror-object-takes-no-parameters-after-defining-new
    def __new__(cls, cache_key):
        return cls.caches[cache_key]

    @classmethod
    def register_cache(cls, cache_class):
        cls.caches[cache_class.cache_key] = cache_class


class CacheBase(object):
    @staticmethod
    def populate(cls):
        raise NotImplementedError()

    @classmethod
    def retrieve(cls):
        return Cache.get(cls.cache_key)

    @classmethod
    def invalidate(cls):
        return Cache.delete(cls.cache_key)


class UsableIngredientCache(CacheBase):
    cache_key = 'ingredient_name_index'

    @classmethod
    def populate(cls):
        # This is still returning all values, just not populating them
        scan_results = IngredientModel.get_usable_ingredients()

        index = []
        for result in scan_results:
            index.append({
                'slug': result.slug,
                'display_name': result.display_name,
                'aliases': result.aliases,
            })

        Cache.set(cls.cache_key, json.dumps(index))


class CocktailNameCache(CacheBase):
    cache_key = 'cocktail_name_index'

    @classmethod
    def populate(cls):
        # This is still returning all values, just not populating them
        scan_results = CocktailModel.get_all()

        index = {}
        for result in scan_results:
            key_alpha = result.slug[0].upper()
            key_entry = {
                'slug': result.slug,
                'display_name': result.display_name
            }
            if key_alpha not in index.keys():
                index[key_alpha] = [key_entry]
            else:
                index[key_alpha].append(key_entry)

        Cache.set(cls.cache_key, json.dumps(index))


Caches.register_cache(UsableIngredientCache)
Caches.register_cache(CocktailNameCache)
