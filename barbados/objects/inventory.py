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
                    ii.add_implied_by(slug)

                # Add the explicit item slug to the list of slugs that this implicit
                # item is implied by. Always >=1.
                ii.add_implied_by(slug)
                self.implicit_items.update({implicit_slug: ii})

    def contains(self, ingredient, implicit=False):
        """
        Determine if a particular ingredient is in this inventory.
        Can't go and recommend something you have explicitly because there
        could be multiple things. Example: implcitly having maraschino-liqueur
        could be true if you have maraska or luxardo. This function shouldn't
        recommend both. Use another endpoint for that.
        :param ingredient: slug of the ingredient to look for.
        :param implicit: Search the implicit list instead (must be populated first).
        :return: Slug of the providing ingredient, otherwise False
        # @TODO refactor this and populate_implicit to bake a list
        # @TODO provide alternatives in the event of direct
        """
        if ingredient in [item.slug for item in self.items]:
            return [ingredient]

        if implicit and ingredient in [item.slug for item in self.implicit_items]:
            return [ingredient]

        return False
