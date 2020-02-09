class IngredientKinds(object):
    """
    https://realpython.com/factory-method-python/
    """
    kinds = {}
    top = None

    # Apparently __call__() didn't work?
    # https://stackoverflow.com/questions/34777773/typeerror-object-takes-no-parameters-after-defining-new
    def __new__(cls, value):
        return cls.kinds[value]

    @classmethod
    def register_kind(cls, kind_class):
        cls.kinds[kind_class.value] = kind_class
        if kind_class.top:
            cls.top = kind_class


class Kind(object):
    top = False


class CategoryKind(Kind):
    value = 'category'
    allowed_parents = [None]
    top = True


class FamilyKind(Kind):
    value = 'family'
    allowed_parents = [CategoryKind.value]


class IngredientKind(Kind):
    value = 'ingredient'
    allowed_parents = [FamilyKind.value, value]


class ProductKind(Kind):
    value = 'product'
    allowed_parents = [IngredientKind.value, FamilyKind.value]


class CustomKind(Kind):
    value = 'custom'
    allowed_parents = [IngredientKind.value, value]


IngredientKinds.register_kind(CategoryKind)
IngredientKinds.register_kind(FamilyKind)
IngredientKinds.register_kind(IngredientKind)
IngredientKinds.register_kind(ProductKind)
IngredientKinds.register_kind(CustomKind)