from barbados.objects.base import BaseObject


class Construction(BaseObject):
    def __init__(self, slug, display_name, default_instructions=None):
        self.slug = slug
        self.display_name = display_name
        self.default_instructions = default_instructions

    def __repr__(self):
        return "Barbados::Objects::Construction[%s]" % self.slug

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('display_name', self.display_name)
        serializer.add_property('default_instructions', self.default_instructions)
