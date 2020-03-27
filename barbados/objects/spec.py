from barbados.serializers import ObjectSerializer


class Spec:
    def __init__(self, name, origin, glassware, components, citations, notes, straw, garnish, instructions, construction):
        self.name = name
        self.origin = origin
        self.glassware = glassware
        self.components = components
        self.citations = citations
        self.notes = notes
        self.straw = straw
        self.garnish = garnish
        self.instructions = instructions
        self.construction = construction

        # @TODO consider ComponentKinds['Primary', 'Accents', 'Garnish']
        # That may be hard to implement since some drinks like the
        # Trinidad Sour are based on traditional accents.
        self.component_counts = {
            'all': len(self.components),
            'primary': self._get_countable_components(),
        }

    def __repr__(self):
        return "<Object:Spec::name=%s>" % self.name

    def _get_countable_components(self):
        count = 0
        for component in self.components:
            if component.countable:
                count += 1
        return count

    def serialize(self, serializer):
        # @TODO expand the other serializers
        serializer.add_property('name', self.name)
        serializer.add_property('origin', self.origin.serialize())
        serializer.add_property('glassware', self.glassware.serialize())
        serializer.add_property('construction', self.construction)
        serializer.add_property('components', [ObjectSerializer.serialize(component, serializer.format) for component in self.components])
        serializer.add_property('component_counts', self.component_counts)
        serializer.add_property('garnish', [ObjectSerializer.serialize(garnish, serializer.format) for garnish in self.garnish])
        serializer.add_property('straw', self.straw)
        serializer.add_property('citations', [citation.serialize() for citation in self.citations])
        serializer.add_property('notes', [note.serialize() for note in self.notes])
        serializer.add_property('instructions', [instruction.serialize() for instruction in self.instructions])
