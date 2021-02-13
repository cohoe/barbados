from barbados.indexers.base import BaseIndexer
from barbados.factories.inventoryfactory import InventoryFactory
from barbados.indexes.inventory import InventoryIndex
from barbados.objects.inventory import Inventory


class InventoryIndexer(BaseIndexer):

    for_class = Inventory
    for_index = InventoryIndex
    factory = InventoryFactory
