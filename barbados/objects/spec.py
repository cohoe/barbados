from barbados.objects.base import BaseObject
from barbados.serializers import ObjectSerializer


class Spec(BaseObject):
    def __init__(self, slug, display_name, origin, glassware, components, citations, notes, straw, garnish, instructions, construction, images):
        self.slug = slug
        self.display_name = display_name
        self.origin = origin
        self.glassware = glassware
        self.components = components
        self.citations = citations
        self.notes = notes
        self.straw = straw
        self.garnish = garnish
        self.instructions = instructions
        self.construction = construction
        self.images = images

    def __repr__(self):
        return "Barbados::Objects::Spec[%s]" % self.slug

    @property
    def component_count(self):
        return len(self.components)

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('display_name', self.display_name)
        serializer.add_property('origin', ObjectSerializer.serialize(self.origin, serializer.format))
        serializer.add_property('glassware', [ObjectSerializer.serialize(glassware, serializer.format) for glassware in self.glassware])
        serializer.add_property('construction', ObjectSerializer.serialize(self.construction, serializer.format))
        serializer.add_property('components', [ObjectSerializer.serialize(component, serializer.format) for component in self.components])
        serializer.add_property('garnish', [ObjectSerializer.serialize(garnish, serializer.format) for garnish in self.garnish])
        serializer.add_property('straw', self.straw)
        serializer.add_property('citations', [ObjectSerializer.serialize(citation, serializer.format) for citation in self.citations])
        serializer.add_property('notes', [ObjectSerializer.serialize(note, serializer.format) for note in self.notes])
        serializer.add_property('instructions', [ObjectSerializer.serialize(instruction, serializer.format) for instruction in self.instructions])
        serializer.add_property('images', [ObjectSerializer.serialize(image, serializer.format) for image in self.images])
