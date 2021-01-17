from barbados.objects.base import BaseObject


class InventoryItem(BaseObject):
    """
    Single item within the inventory.
    """
    def __init__(self, slug, parent=None):
        self.slug = slug
        self.substitutes = []
        self.parent = parent

    def add_substitute(self, slug):
        """
        Add an ingredient by slug as a substitute of this item.
        :param slug: Slug of the ingredient to add as the parent.
        :return: List of substitute slugs for this item.
        """
        if slug not in self.substitutes:
            self.substitutes.append(slug)

        return self.substitutes

    def __repr__(self):
        return "Barbados::Objects::InventoryItem[%s]" % self.slug

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('substitutes', self.substitutes)
        serializer.add_property('parent', self.parent)
