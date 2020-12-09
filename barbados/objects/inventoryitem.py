class InventoryItem:
    def __init__(self, slug, implied_by=None):
        self.slug = slug
        self.implied_by = None
        if implied_by and implied_by != slug:
            self.implied_by = implied_by

    def __repr__(self):
        return "Barbados::Objects::InventoryItem[%s]" % self.slug

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('implied_by', self.implied_by)
