class InventoryItem:
    def __init__(self, slug):
        self.slug = slug
        # self.implied_by = [slug]
        self.implied_by = []

    def add_implied_by(self, slug):
        if slug not in self.implied_by:
            self.implied_by.append(slug)

        return self.implied_by

    def __repr__(self):
        return "Barbados::Objects::InventoryItem[%s]" % self.slug

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('implied_by', self.implied_by)
