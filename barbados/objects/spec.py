from barbados.serializers import ObjectSerializer


# @TODO this belongs in search
# class SpecComponentCounts:
#     # @TODO consider ComponentKinds['Primary', 'Accents', 'Garnish']
#     # That may be hard to implement since some drinks like the
#     # Trinidad Sour are based on traditional accents.
#     def __init__(self, components, garnish):
#         self.components = components
#         self.garnish = garnish
#         self.counts = {
#             'all': len(self.components),
#             'primary': self._get_countable_components(),
#             'garnish': len(self.garnish),
#         }
#
#     def _get_countable_components(self):
#         count = 0
#         for component in self.components:
#             if component.countable:
#                 count += 1
#         return count
#
#     def serialize(self, serializer):
#         for key in self.counts.keys():
#             serializer.add_property(key, self.counts[key])


class Spec:
    def __init__(self, slug, display_name, origin, glassware, components, citations, notes, straw, garnish, instructions, construction):
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
        # self.component_counts = SpecComponentCounts(components, garnish)

    def __repr__(self):
        return "Barbados::Objects::Spec[%s]" % self.slug

    def serialize(self, serializer):
        # @TODO expand the other serializers
        serializer.add_property('slug', self.slug)
        serializer.add_property('display_name', self.display_name)
        serializer.add_property('origin', ObjectSerializer.serialize(self.origin, serializer.format))
        serializer.add_property('glassware', [ObjectSerializer.serialize(glassware, serializer.format) for glassware in self.glassware])
        serializer.add_property('construction', ObjectSerializer.serialize(self.construction, serializer.format))
        serializer.add_property('components', [ObjectSerializer.serialize(component, serializer.format) for component in self.components])
        # serializer.add_property('component_counts', ObjectSerializer.serialize(self.component_counts, serializer.format))
        serializer.add_property('garnish', [ObjectSerializer.serialize(garnish, serializer.format) for garnish in self.garnish])
        serializer.add_property('straw', self.straw)
        serializer.add_property('citations', [ObjectSerializer.serialize(citation, serializer.format) for citation in self.citations])
        serializer.add_property('notes', [ObjectSerializer.serialize(note, serializer.format) for note in self.notes])
        serializer.add_property('instructions', [ObjectSerializer.serialize(instruction, serializer.format) for instruction in self.instructions])
