from barbados.factories.base import BaseFactory
from barbados.text import DisplayName
from barbados.objects.inventory import Inventory
from barbados.objects.inventoryitem import InventoryItem
from barbados.exceptions import ValidationException
from barbados.services.logging import Log
from uuid import uuid4


class InventoryFactory(BaseFactory):

    required_keys = {
        'id': uuid4(),
        'items': list(),
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

        Log.info("Old value for %s is %s" % (value_key, old_value))
        if not raw_input:
            new_value = DisplayName('Unnamed Inventory')
        elif type(old_value) is str:
            new_value = DisplayName(old_value)
        else:
            raise ValidationException("Bad display name given for inventory (%s)" % old_value)

        Log.info("New value for %s is %s" % (value_key, new_value))
        raw_input.update({value_key: new_value})
        return raw_input

    @staticmethod
    def _parse_items(raw_input):
        value_key = 'items'
        old_value = raw_input.get(value_key)

        Log.info("Old value for %s is %s" % (value_key, old_value))
        new_value = []
        for raw_item in raw_input.get(value_key):
            ii = InventoryItem(**raw_item)
            new_value.append(ii)

        Log.info("New value for %s is %s" % (value_key, new_value))
        raw_input.update({value_key: new_value})
        return raw_input