class InventoryItem:
    def __init__(self, slug):
        self.slug = slug

    def __repr__(self):
        return "Barbados::Objects::InventoryItem[%s]" % self.slug

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
