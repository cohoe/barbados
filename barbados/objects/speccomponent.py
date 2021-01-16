from barbados.objects.text import DisplayName
from barbados.serializers import ObjectSerializer


class SpecComponent:
    """
    Someday the direct name part might be able to go away.
    """
    def __init__(self, slug, display_name=None, quantity=None, unit=None, notes=None):
        if not display_name:
            display_name = DisplayName(slug)
        if not notes:
            notes = []
        self.slug = slug
        self.display_name = display_name
        self.quantity = quantity
        self.unit = unit
        self.notes = notes

    def __repr__(self):
        return "Barbados::Objects::SpecComponent[%s]" % self.slug

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('display_name', self.display_name)
        serializer.add_property('quantity', self.quantity, even_if_empty=False)
        serializer.add_property('unit', self.unit, even_if_empty=False)
        serializer.add_property('notes', [ObjectSerializer.serialize(note, serializer.format) for note in self.notes])
