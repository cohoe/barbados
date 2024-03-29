from barbados.factories.base import BaseFactory
from barbados.objects.text import DisplayName
from barbados.objects.inventory import Inventory
from barbados.objects.inventoryitem import InventoryItem
from barbados.exceptions import FactoryException
from barbados.models.inventory import InventoryModel
from barbados.caches.ingredienttree import IngredientTreeCache
from barbados.validators.inventorymodel import InventoryModelValidator
from barbados.indexes.inventory import InventoryIndex
from barbados.factories.parser import FactoryParser


class InventoryFactory(BaseFactory):
    _model = InventoryModel
    _validator = InventoryModelValidator
    _index = InventoryIndex

    required_keys = {
        'items': dict(),
        'implicit_items': dict(),
    }

    @staticmethod
    def raw_to_obj(raw):
        raw_inventory = InventoryFactory.sanitize_raw(raw_input=raw, required_keys=InventoryFactory.required_keys)

        # Beware the Python dict copying bullshit!
        raw_inventory = FactoryParser.parse_id(raw_inventory)
        raw_inventory = FactoryParser.parse_display_name(raw_inventory)
        raw_inventory = InventoryFactory._parse_items(raw_inventory)

        # Build the object
        i = Inventory(**raw_inventory)
        return i

    @staticmethod
    def _parse_items(raw_input):
        value_key = 'items'
        items = raw_input.get(value_key)

        # Log.info("Old value for %s is %s" % (value_key, old_value))
        # new_value = []
        for raw_item in items.keys():
            ii = InventoryItem(slug=raw_item)
            # new_value.append(ii)
            items.update({raw_item: ii})

        # Log.info("New value for %s is %s" % (value_key, new_value))
        raw_input.update({value_key: items})
        return raw_input

    @classmethod
    def produce_obj(cls, id, expand=False):
        i = super().produce_obj(id=id)
        if expand:
            tree = IngredientTreeCache.retrieve()
            i.expand(tree)

        return i

    @classmethod
    def obj_to_index(cls, obj):
        """
        This is custom because elasticsearch_dsl doesn't have flattened
        support yet. See the InventoryIndex class for more details.
        :param obj:
        :return:
        """
        index = super().obj_to_index(obj)
        delattr(index, 'items')
        delattr(index, 'implicit_items')
        return index

    @classmethod
    def index_to_obj(cls, indexable):
        raise Exception("Not supported")
