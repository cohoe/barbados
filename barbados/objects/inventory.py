import copy
from barbados.serializers import ObjectSerializer
from barbados.services.logging import Log
from barbados.objects.inventoryitem import InventoryItem


class Inventory:
    def __init__(self, id, display_name, items):
        self.id = id
        self.display_name = display_name
        self.items = items
        self.implicit_items = []
        self.slug = id  # Backwards Compatibility. This is not in the serializer.

    def __repr__(self):
        return "Barbados::Objects::Inventory[%s]" % self.id

    def serialize(self, serializer):
        serializer.add_property('id', str(self.id))
        serializer.add_property('display_name', self.display_name)
        serializer.add_property('items', [ObjectSerializer.serialize(item, serializer.format) for item in self.items])
        serializer.add_property('implicit_items', [ObjectSerializer.serialize(item, serializer.format) for item in self.implicit_items])

    def populate_implicit_items(self, tree):
        Log.info("Generating implicit items for inventory %s" % self.id)
        full_items = []
        for item in self.items:
            implicit_items = tree.implies(item.slug)
            # Log.info("Implicit items for %s are: %s" % (item, implicit_items))
            [full_items.append(InventoryItem(implicit_item)) for implicit_item in implicit_items]

        self.implicit_items = full_items

    def contains(self, ingredient, implicit=False):
        """
        Determine if a particular ingredient is in this inventory.
        :param ingredient: slug of the ingredient to look for.
        :param implicit: Search the implicit list instead (must be populated first).
        :return: Boolean
        """
        if ingredient in [item.slug for item in self.items]:
            return True

        if implicit and ingredient in [item.slug for item in self.implicit_items]:
            return True

        return False
