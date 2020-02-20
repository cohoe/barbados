from barbados.objects.ingredientkinds import IngredientKinds


class Ingredient:
    def __init__(self, slug, display_name, kind, parent=None, aliases=None):
        if aliases is None:
            aliases = []
        self.slug = slug
        self.display_name = display_name
        self.kind = IngredientKinds(kind)
        self.parent = parent
        self.aliases = aliases

    def serialize(self):
        return ({
            'slug': self.slug,
            'display_name': self.display_name,
            'kind': self.kind.value,
            'parent': self.parent,
            'aliases': self.aliases,
        })
