from barbados.serializers import ObjectSerializer


class Cocktail:
    def __init__(self, display_name, origin, specs, citations, notes, tags, slug, images):
        self.display_name = display_name
        self.origin = origin
        self.specs = specs
        self.citations = citations
        self.notes = notes
        self.tags = tags
        self.slug = slug
        self.images = images

    @property
    def spec_count(self):
        return len(self.specs)

    def __repr__(self):
        return "Barbados::Objects::Cocktail[%s]>" % self.slug

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('display_name', self.display_name)
        serializer.add_property('origin', ObjectSerializer.serialize(self.origin, serializer.format))
        serializer.add_property('specs', [ObjectSerializer.serialize(spec, serializer.format) for spec in self.specs])
        serializer.add_property('spec_count', self.spec_count)
        serializer.add_property('citations', [ObjectSerializer.serialize(citation, serializer.format) for citation in self.citations])
        serializer.add_property('notes', [ObjectSerializer.serialize(note, serializer.format) for note in self.notes])
        serializer.add_property('images', [ObjectSerializer.serialize(image, serializer.format) for image in self.images])
