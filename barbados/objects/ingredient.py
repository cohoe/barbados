import enum


class IngredientTypeEnum(enum.Enum):
    CATEGORY = 'category'
    FAMILY = 'family'
    INGREDIENT = 'ingredient'


class Ingredient:
    def __init__(self, slug, display_name, type, parent=None):
        self.slug = slug
        self.display_name = display_name
        self.type_ = IngredientTypeEnum(type)
        self.parent = parent

    def serialize(self):
        return ({
            'slug': self.slug,
            'display_name': self.display_name,
            'type': self.type_.value,
            'parent': self.parent
        })
