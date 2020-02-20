from barbados.objects.ingredientkinds import IngredientKinds


class Ingredient:
    def __init__(self, slug, display_name, kind, parent=None, aliases=None, elements=None):
        if aliases is None:
            aliases = []

        if elements is None:
            elements = []

        self.slug = slug
        self.display_name = display_name
        self.kind = IngredientKinds(kind)
        self.parent = parent
        self.aliases = aliases
        self.elements = elements

    def serialize(self):
        return ({
            'slug': self.slug,
            'display_name': self.display_name,
            'kind': self.kind.value,
            'parent': self.parent,
            'aliases': self.aliases,
            'elements': self.elements,
        })
