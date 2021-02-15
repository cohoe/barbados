import json
from barbados.caches import Caches
from barbados.caches.base import CacheBase
from barbados.services.cache import CacheService
from barbados.serializers import ObjectSerializer

from barbados.models.cocktail import CocktailModel
from barbados.models.inventory import InventoryModel
from barbados.models.ingredient import IngredientModel
from barbados.models.drinklist import DrinkListModel
from barbados.models.construction import ConstructionModel

from barbados.factories.cocktail import CocktailFactory
from barbados.factories.inventory import InventoryFactory
from barbados.factories.ingredient import IngredientFactory
from barbados.factories.drinklist import DrinkListFactory
from barbados.factories.construction import ConstructionFactory


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
        cache_objects = []
        objects = cls.factory_class.produce_all_objs()
        for result_object in objects:
            cache_objects.append(ObjectSerializer.serialize(result_object, 'dict'))

        CacheService.set(cls.cache_key, json.dumps(cache_objects))


class CocktailScanCache(TableScanCache):
    cache_key = 'cocktail_scan_cache'
    model_class = CocktailModel
    factory_class = CocktailFactory


class IngredientScanCache(TableScanCache):
    cache_key = 'ingredient_scan_cache'
    model_class = IngredientModel
    factory_class = IngredientFactory


class DrinkListScanCache(TableScanCache):
    cache_key = 'drinklist_scan_cache'
    model_class = DrinkListModel
    factory_class = DrinkListFactory


class InventoryScanCache(TableScanCache):
    cache_key = 'inventory_scan_cache'
    model_class = InventoryModel
    factory_class = InventoryFactory


class ConstructionScanCache(TableScanCache):
    cache_key = 'construction_scan_cache'
    model_class = ConstructionModel
    factory_class = ConstructionFactory


Caches.register_cache(CocktailScanCache)
Caches.register_cache(IngredientScanCache)
Caches.register_cache(DrinkListScanCache)
Caches.register_cache(InventoryScanCache)
Caches.register_cache(ConstructionScanCache)
