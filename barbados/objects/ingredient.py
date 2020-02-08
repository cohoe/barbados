from barbados.constants import IngredientKinds


class Ingredient:
    def __init__(self, slug, display_name, kind, parent=None):
        self.slug = slug
        self.display_name = display_name
        self.kind = IngredientKinds(kind)
        self.parent = parent

    def serialize(self):
        return ({
            'slug': self.slug,
            'display_name': self.display_name,
            'kind': self.kind.value,
            'parent': self.parent
        })
