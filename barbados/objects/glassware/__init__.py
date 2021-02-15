from barbados.objects.base import BaseObject
from barbados.serializers import ObjectSerializer


class Glassware(BaseObject):
    def __init__(self, slug, display_name=None, description=None, images=None):
        if images is None:
            images = []
        self.slug = slug
        self.display_name = display_name
        self.description = description
        self.images = images

    def __repr__(self):
        return "Barbados::Objects:Glassware[%s]" % self.slug

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('display_name', self.display_name)
        serializer.add_property('description', self.description)
        serializer.add_property('images', [ObjectSerializer.serialize(i, serializer.format) for i in self.images])
