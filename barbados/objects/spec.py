from barbados.serializers import ObjectSerializer


class Spec:
    def __init__(self, name, origin, glassware, ingredients, citations, notes, straw, garnish, instructions, construction):
        self.name = name
        self.origin = origin
        self.glassware = glassware
        self.ingredients = ingredients
        self.citations = citations
        self.notes = notes
        self.straw = straw
        self.garnish = garnish
        self.instructions = instructions
        self.construction = construction

    def __repr__(self):
        return "<Object:Spec::name=%s>" % self.name

    @property
    def ingredient_count(self):
        count = 0
        for ingredient in self.ingredients:
            if 'bitters' not in ingredient.name.lower():
                count += 1
        return count

    def serialize(self, serializer):
        # @TODO expand the other serializers
        # @TODO format from the base serializer
        serializer.add_property('name', self.name)
        serializer.add_property('origin', self.origin.serialize())
        serializer.add_property('glassware', self.glassware.serialize())
        serializer.add_property('construction', self.construction)
        serializer.add_property('ingredients', [ingredient.serialize() for ingredient in self.ingredients])
        serializer.add_property('ingredient_count', self.ingredient_count)
        serializer.add_property('garnish', [ObjectSerializer.serialize(garnish, 'dict') for garnish in self.garnish])
        serializer.add_property('straw', self.straw)
        serializer.add_property('citations', [citation.serialize() for citation in self.citations])
        serializer.add_property('notes', [note.serialize() for note in self.notes])
