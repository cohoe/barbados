class InventoryItem:
    """
    Single item within the inventory.
    """
    def __init__(self, slug):
        self.slug = slug
        self.substitutes = []

    def add_substitute(self, slug):
        """
        Add an ingredient by slug as a substitute of this item.
        :param slug:
        :return:
        """
        if slug not in self.substitutes:
            self.substitutes.append(slug)

        return self.substitutes

    def __repr__(self):
        return "Barbados::Objects::InventoryItem[%s]" % self.slug

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('substitutes', self.substitutes)
