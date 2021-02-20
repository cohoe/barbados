from barbados.objects.base import BaseObject
from barbados.serializers import ObjectSerializer


class List(BaseObject):
    """
    I really hope this class name doesn't bite me.
    """
    def __init__(self, id, display_name, items):
        self.id = id
        self.display_name = display_name
        self.items = items
        # @TODO notes?

    def add_item(self, item):
        items_with_keys = {i.cocktail_slug: i for i in self.items}
        if item.cocktail_slug in items_with_keys.keys():
            raise KeyError("%s is already an item of %s" % (item.cocktail_slug, self.id))
        self.items.append(item)

    def remove_item(self, slug):
        items_with_keys = {i.cocktail_slug: i for i in self.items}
        if slug not in items_with_keys.keys():
            raise KeyError("%s is not an item of %s" % (slug, self.id))
        self.items.remove(items_with_keys[slug])

    def __repr__(self):
        return "Barbados::Objects::List[%s]" % self.id

    def serialize(self, serializer):
        serializer.add_property('id', str(self.id))
        serializer.add_property('display_name', self.display_name)
        serializer.add_property('items', [ObjectSerializer.serialize(item, serializer.format) for item in self.items])
