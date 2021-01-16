from barbados.objects.base import BarbadosObject
from barbados.objects.ingredientkinds import IngredientKinds


class Ingredient(BarbadosObject):
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

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('display_name', self.display_name)
        serializer.add_property('kind', self.kind.value)
        serializer.add_property('parent', self.parent)
        serializer.add_property('aliases', self.aliases)
        serializer.add_property('elements', self.elements)
