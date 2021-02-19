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

    def __repr__(self):
        return "Barbados::Objects::List[%s]" % self.id

    def serialize(self, serializer):
        serializer.add_property('id', str(self.id))
        serializer.add_property('display_name', self.display_name)
        serializer.add_property('items', [ObjectSerializer.serialize(item, serializer.format) for item in self.items])
