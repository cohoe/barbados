from barbados.serializers import ObjectSerializer


class Menu:
    def __init__(self, slug, display_name, items):
        self.slug = slug
        self.display_name = display_name
        self.items = items

    def __repr__(self):
        return "Barbados::Objects::Menu[%s]" % self.slug

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('display_name', self.display_name)
        serializer.add_property('items', [ObjectSerializer.serialize(item, serializer.format) for item in self.items])
