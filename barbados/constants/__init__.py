from aenum import Enum, extend_enum


class IngredientKinds(Enum):
    """
    https://stackoverflow.com/questions/28126314/adding-members-to-python-enums/35899963
    """
    pass


class CategoryKind:
    extend_enum(IngredientKinds, 'CATEGORY', 'category')


class FamilyKind:
    extend_enum(IngredientKinds, 'FAMILY', 'family')


class IngredientKind:
    extend_enum(IngredientKinds, 'INGREDIENT', 'ingredient')


class ProductKind:
    extend_enum(IngredientKinds, 'PRODUCT', 'product')


class CustomKind:
    extend_enum(IngredientKinds, 'CUSTOM', 'custom')


TopIngredientKind = IngredientKinds.CATEGORY
