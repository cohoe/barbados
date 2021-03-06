from barbados.objects.base import BaseObject
from barbados.serializers import ObjectSerializer
from barbados.objects.inventoryitem import InventoryItem


class Inventory(BaseObject):
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
        serializer.add_property('implicit_items',
                                {slug: ObjectSerializer.serialize(ii, serializer.format) for slug, ii in self.implicit_items.items()})

    def expand(self, tree):
        """
        Fill in the substitutions and implicit_items for this inventory. Computationally
        intensive and lots of data that shouldn't be stored in the database so this is
        a separate function that users needs to call.
        :param tree: IngredientTree instance.
        :return: None
        """
        # print("INFLATION")
        for slug, item in self.items.items():
            # Substitutes are anything that is implied by this item.
            # and contained within the explicit inventory items.
            # If you need guidance beyond that you should use the
            # ingredients/{slug}/substitution to help you find something
            # appropriate.
            tree_implied_slugs = tree.implies(slug)
            # print("%s => %s" % (slug, tree_implied_slugs)) if 'gin' in slug or 'aquavit' in slug else None
            for implied_slug in tree_implied_slugs:
                try:
                    # We've already created an implied item based on this explicit item.
                    ii = self.implicit_items[implied_slug]
                except KeyError:
                    # This explicit ingredient is adding a new implied ingredient to the
                    # inventory. Cool!
                    ii = InventoryItem(slug=implied_slug)

                # Add the explicit item slug to the list of slugs that this implicit
                # item is implied by.
                ii.add_substitute(slug)

                # Fill in the parent if it hasn't already. See below for more.
                if not ii.parent:
                    ii.parent = tree.parent(slug).tag

                # Update the object in the implicit_items dictionary.
                self.implicit_items.update({implied_slug: ii})

                # If the implied item is in the explicit inventory, then it can be
                # suggested. Implicit suggestions are handled for other resolution
                # types so we don't need to go digging around for other things to
                # use here. I think....
                #
                # I'm still not convinced I don't need to go searching through the
                # implicits once those are populated. Need to make an inventory
                # based on all generics and compare that to certain generic specs
                # and see if the results match expectations.
                if implied_slug in self.items.keys():
                    item.add_substitute(implied_slug)

            # Fill in the parent, regardless of if it's something we have or not.
            # Will give the user a pointer.
            item.parent = tree.parent(slug).tag

    def contains(self, ingredient, implicit=False):
        """
        Determine if a particular ingredient is in this inventory.
        :param ingredient: Slug of the ingredient to look for.
        :param implicit: Bootlean of whether to be explicit or implicit.
        :return: Boolean
        """
        if ingredient in self.items.keys():
            return True

        if implicit and ingredient in self.implicit_items.keys():
            return True

        return False

    def substitutes(self, ingredient, implicit=False):
        """
        Return a list of all InventoryItem slugs that are substitutes for
        this ingredient. User specifies whether they want the implicit items
        or just the explicit ones.
        :param ingredient: Slug of the ingredient to look for.
        :param implicit: Boolean of whether to be explicit or implicit.
        :return: List
        """
        if ingredient in self.items.keys():
            # We don't pre-calculate inventory-derived substitutes
            # so we have to go fetch.
            # print(self.items.get(ingredient).substitutes)
            return self.items.get(ingredient).substitutes

        if implicit and ingredient in self.implicit_items.keys():
            # print(self.implicit_items.get(ingredient).substitutes) if 'gin' in ingredient else None
            return self.implicit_items.get(ingredient).substitutes

        return []
