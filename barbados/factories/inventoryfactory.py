from barbados.factories.base import BaseFactory
from barbados.objects.text import DisplayName
from barbados.objects.inventory import Inventory
from barbados.objects.inventoryitem import InventoryItem
from barbados.exceptions import ValidationException
from barbados.services.logging import LogService
from uuid import uuid4
from barbados.models.inventorymodel import InventoryModel
from barbados.caches.ingredienttree import IngredientTreeCache


class InventoryFactory(BaseFactory):
    _model = InventoryModel

    required_keys = {
        'id': uuid4(),
        'items': dict(),
        'implicit_items': dict(),
    }

    @staticmethod
    def raw_to_obj(raw):
        raw_inventory = InventoryFactory.sanitize_raw(raw_input=raw, required_keys=InventoryFactory.required_keys)

        # Beware the Python dict copying bullshit!
        raw_inventory = InventoryFactory._parse_display_name(raw_inventory)
        raw_inventory = InventoryFactory._parse_items(raw_inventory)

        # Build the object
        i = Inventory(**raw_inventory)
        return i

    @staticmethod
    def _parse_display_name(raw_input):
        value_key = 'display_name'
        old_value = raw_input.get(value_key)

        # Log.info("Old value for %s is %s" % (value_key, old_value))
        if not raw_input:
            new_value = DisplayName('Unnamed Inventory')
        elif type(old_value) is str:
            new_value = DisplayName(old_value)
        else:
            raise ValidationException("Bad display name given for inventory (%s)" % old_value)

        # Log.info("New value for %s is %s" % (value_key, new_value))
        raw_input.update({value_key: new_value})
        return raw_input

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
    def produce_obj(cls, session, id, expand=False):
        i = super().produce_obj(session=session, id=id)
        if expand:
            tree = IngredientTreeCache.retrieve()
            i.expand(tree)

        return i
