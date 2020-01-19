class Spec:
    def __init__(self, name, origin, glassware, ingredients, citations, notes, straw, garnish, instructions):
        self.name = name
        self.origin = origin
        self.glassware = glassware
        self.ingredients = ingredients
        self.citations = citations
        self.notes = notes
        self.straw = straw
        self.garnish = garnish
        self.instructions = instructions

    def __repr__(self):
        return "<Object:Spec::name=%s>" % self.name

    @property
    def ingredient_count(self):
        count = 0
        for ingredient in self.ingredients:
            if 'bitters' not in ingredient.name.lower():
                count += 1
        return count

    def serialize(self):
        ser = {
            'name': self.name,
            'origin': self.origin.serialize(),
            'glassware': self.glassware.serialize(),
            'ingredients': [ingredient.serialize() for ingredient in self.ingredients],
            'ingredient_count': self.ingredient_count,
            'instructions': [instruction.serialize() for instruction in self.instructions],
            'garnish': [garnish.serialize() for garnish in self.garnish],
            'straw': self.straw,
            'citations': [citation.serialize() for citation in self.citations],
            'notes': [note.serialize() for note in self.notes],
        }

        return ser
