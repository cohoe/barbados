import copy
from barbados.serializers import ObjectSerializer
from barbados.services.logging import Log
from barbados.objects.inventoryitem import InventoryItem


class Inventory:
    def __init__(self, id, display_name, items, implicit_items=None):
        self.id = id
        self.display_name = display_name
        self.items = items
        self.implicit_items = {}  # You cannot __init__ this.
        self.slug = id  # Backwards Compatibility. This is not in the serializer.

    def __repr__(self):
        return "Barbados::Objects::Inventory[%s]" % self.id

    def serialize(self, serializer):
        serializer.add_property('id', str(self.id))
        serializer.add_property('display_name', self.display_name)
        serializer.add_property('items', {slug: ObjectSerializer.serialize(ii, serializer.format) for slug, ii in self.items.items()})
        serializer.add_property('implicit_items', {slug: ObjectSerializer.serialize(ii, serializer.format) for slug, ii in self.implicit_items.items()})

    def populate_implicit_items(self, tree):
        # @TODO populate substitutes for direct as well using common parent.
        for slug in self.items.keys():
            tree_implicit_slugs = tree.implies(slug)
            for implicit_slug in tree_implicit_slugs:
                try:
                    # We've already created an implied item based on this explicit
                    # item.
                    ii = self.implicit_items[implicit_slug]
                    # self.implicit_items.update({implicit_slug: ii})
                except KeyError:
                    # This explicit ingredient is adding a new implied ingreident to the
                    # inventory. Cool!
                    ii = InventoryItem(slug=implicit_slug)
                    # ii.add_implied_by(slug)

                # Add the explicit item slug to the list of slugs that this implicit
                # item is implied by. Always >=1.
                # if implicit_slug in self.items.keys():
                # print("%s is DIRECT" % implicit_slug) if implicit_slug in self.items.keys() else None
                # print("%s is IMPLIOED" % implicit_slug) if implicit_slug not in self.items.keys() else None
                ii.add_implied_by(slug)
                self.implicit_items.update({implicit_slug: ii})

        # print(self.implicit_items.get('sweet-vermouth').implied_by)

    def contains(self, ingredient, implicit=False):
        """
        Determine if a particular ingredient is in this inventory.
        :param ingredient: slug of the ingredient to look for in the explicit dict.
        :param implicit: Search the implicit dict instead (must be populated first).
        :return: List of all slugs you have in the inventory that are implied by
                 the given ingredient, otherwise False
                 # @TODO refactor for contains vs substitutes
        """
        if ingredient in self.items.keys():
            return True

        if implicit and ingredient in self.implicit_items.keys():
            return True

        return False

    def substitutes(self, ingredient, implicit=False):
        if ingredient in self.items.keys():
            return self.items.get(ingredient).implied_by

        if implicit and ingredient in self.implicit_items.keys():
            return self.implicit_items.get(ingredient).implied_by

        return False
