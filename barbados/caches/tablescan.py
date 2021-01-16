import json
from barbados.caches import Caches
from barbados.caches.base import CacheBase
from barbados.services.registry import RegistryService
from barbados.services.cache import CacheService
from barbados.serializers import ObjectSerializer

from barbados.models.cocktail import CocktailModel
from barbados.models.inventory import InventoryModel
from barbados.models.ingredient import IngredientModel
from barbados.models.menu import MenuModel

from barbados.factories.cocktailfactory import CocktailFactory
from barbados.factories.inventoryfactory import InventoryFactory
from barbados.factories.ingredientfactory import IngredientFactory
from barbados.factories.menufactory import MenuFactory


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
        pgconn = RegistryService.get_database_connection()

        with pgconn.get_session() as session:
            cache_objects = []
            objects = cls.factory_class.produce_all_objs(session=session)
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


class MenuScanCache(TableScanCache):
    cache_key = 'menu_scan_cache'
    model_class = MenuModel
    factory_class = MenuFactory


class InventoryScanCache(TableScanCache):
    cache_key = 'inventory_scan_cache'
    model_class = InventoryModel
    factory_class = InventoryFactory


Caches.register_cache(CocktailScanCache)
Caches.register_cache(IngredientScanCache)
Caches.register_cache(MenuScanCache)
Caches.register_cache(InventoryScanCache)
