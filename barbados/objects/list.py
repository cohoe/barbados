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

    @property
    def items_dict(self):
        return {i.cocktail_slug: i for i in self.items}

    def get_item(self, slug):
        return self.items_dict[slug]

    def add_item(self, item):
        if item.cocktail_slug in self.items_dict.keys():
            raise KeyError("%s is already an item of %s" % (item.cocktail_slug, self.id))
        self.items.append(item)

    def remove_item(self, slug):
        if slug not in self.items_dict.keys():
            raise KeyError("%s is not an item of %s" % (slug, self.id))
        self.items.remove(self.items_dict[slug])

    def replace_item(self, item):
        if item.cocktail_slug not in self.items_dict.keys():
            raise KeyError("%s is not an item of %s" % (item.cocktail_slug, self.id))
        for index, list_item in enumerate(self.items):
            if list_item.cocktail_slug == item.cocktail_slug:
                self.items[index] = item
                return item
        raise Exception("Did not process %s for %s" % (item.cocktail_slug, self.id))

    def __repr__(self):
        return "Barbados::Objects::List[%s]" % self.id

    def serialize(self, serializer):
        serializer.add_property('id', str(self.id))
        serializer.add_property('display_name', self.display_name)
        serializer.add_property('items', [ObjectSerializer.serialize(item, serializer.format) for item in self.items])
