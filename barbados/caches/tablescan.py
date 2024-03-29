import json
from barbados.caches import Caches
from barbados.caches.base import CacheBase
from barbados.services.cache import CacheService
from barbados.serializers import ObjectSerializer

from barbados.models.cocktail import CocktailModel
from barbados.models.inventory import InventoryModel
from barbados.models.ingredient import IngredientModel
from barbados.models.list import ListModel
from barbados.models.construction import ConstructionModel
from barbados.models.glassware import GlasswareModel

from barbados.factories.cocktail import CocktailFactory
from barbados.factories.inventory import InventoryFactory
from barbados.factories.ingredient import IngredientFactory
from barbados.factories.list import ListFactory
from barbados.factories.construction import ConstructionFactory
from barbados.factories.glassware import GlasswareFactory


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

    @classmethod
    def retrieve(cls):
        """
        Retrieve and decode the scan.
        :return: Complex object.
        """
        # https://www.geeksforgeeks.org/python-call-parent-class-method/
        return json.loads(super().retrieve())


class CocktailScanCache(TableScanCache):
    cache_key = 'cocktail_scan_cache'
    model_class = CocktailModel
    factory_class = CocktailFactory


class IngredientScanCache(TableScanCache):
    cache_key = 'ingredient_scan_cache'
    model_class = IngredientModel
    factory_class = IngredientFactory


class ListScanCache(TableScanCache):
    cache_key = 'list_scan_cache'
    model_class = ListModel
    factory_class = ListFactory


class InventoryScanCache(TableScanCache):
    cache_key = 'inventory_scan_cache'
    model_class = InventoryModel
    factory_class = InventoryFactory


class ConstructionScanCache(TableScanCache):
    cache_key = 'construction_scan_cache'
    model_class = ConstructionModel
    factory_class = ConstructionFactory


class GlasswareScanCache(TableScanCache):
    cache_key = 'glassware_scan_cache'
    model_class = GlasswareModel
    factory_class = GlasswareFactory


Caches.register_cache(CocktailScanCache)
Caches.register_cache(IngredientScanCache)
Caches.register_cache(ListScanCache)
Caches.register_cache(InventoryScanCache)
Caches.register_cache(ConstructionScanCache)
Caches.register_cache(GlasswareScanCache)
