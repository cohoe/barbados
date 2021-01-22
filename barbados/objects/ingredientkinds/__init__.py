class IngredientKinds(object):
    """
    https://realpython.com/factory-method-python/
    """
    kinds = {}
    top = None
    index = None
    usables = []
    implicits = []

    # Apparently __call__() didn't work?
    # https://stackoverflow.com/questions/34777773/typeerror-object-takes-no-parameters-after-defining-new
    def __new__(cls, value):
        return cls.kinds[value]

    @classmethod
    def register_kind(cls, kind_class):
        cls.kinds[kind_class.value] = kind_class
        if kind_class.top:
            cls.top = kind_class
        if kind_class.usable:
            cls.usables.append(kind_class)
        if kind_class.index:
            cls.index = kind_class
        if kind_class.implicit:
            cls.implicits.append(kind_class)


class Kind(object):
    # Top indicates if this kind is the highest level of the tree.
    top = False

    # Usable indicates if ingredients of this kind are eligible to be
    # referenced in recipes.
    usable = False

    # Index indicates if this kind acts like an index (view). It can have
    # no direct children but can list "adopted" children (called Elements)
    # as a way to provide alternative collections of ingredients.
    index = False

    # Implicit means that this kind of ingredient qualifies as "implicitly
    # available" if you have one of its children.
    implicit = True


class CategoryKind(Kind):
    """
    High-level classifiers. New ones should be pretty rare.

    Examples:
        * Animal
        * Fruits
        * Spirits
    """
    value = 'category'
    allowed_parents = [None]
    top = True
    implicit = False


class FamilyKind(Kind):
    """
    High-level container of a genre of products. This serves as the terminus
    level for any suggestions. If you have a Product or Ingredient under a Family
    you can generally swap between them without much effort. Families can have
    several levels hence they can descend from each other.

    Examples:
        * Sugarcane
        * Citrus
        * Dairy
    """
    value = 'family'
    allowed_parents = [CategoryKind.value, value]
    usable = True
    implicit = False


class IngredientKind(Kind):
    """
    Any non-specific component of a recipe. These can range in being rather
    broad to de-facto products. Since these are the middle tier of the tree
    they should include the various "subcategories" of a particular spirit
    or family.

    Examples:
        * Aged Rum
        * Irish Whiskey
        * Reposado Tequila
        * "Condensed Milk" and "Sweetened Condensed Milk"
    """
    value = 'ingredient'
    allowed_parents = [FamilyKind.value, value]
    usable = True


class ProductKind(Kind):
    """
    Products are specific brands/releases, anything that is as specific to a
    purchasable SKU that you could find in a store. Nothing house-made or custom
    should belong here.

    Examples:
        * The Dead Rabbit Irish Whiskey
        * El Dorado 12-year Rum
    """
    value = 'product'
    allowed_parents = [IngredientKind.value, FamilyKind.value, value]
    usable = True


class CustomKind(Kind):
    """
    Products or Ingredients that are modified or custom produced by a specific
    venue or bartender. Includes infusions or house blends.

    Examples:
        * House Orange Bitters
        * Jalapeno-infused Tequila
        * Szechuan-peppercorn infused gin
    """
    value = 'custom'
    allowed_parents = [IngredientKind.value, ProductKind.value, FamilyKind.value, value]
    usable = True


class IndexKind(Kind):
    """
    Loose classifications of various ingredients that present an alternative
    view of the tree. They cannot have children.

    Examples:
        * Jamaican Rum
        * Peaty Scotch
    """
    value = 'index'
    allowed_parents = [FamilyKind.value, IngredientKind.value]
    usable = True
    index = True


IngredientKinds.register_kind(CategoryKind)
IngredientKinds.register_kind(FamilyKind)
IngredientKinds.register_kind(IngredientKind)
IngredientKinds.register_kind(ProductKind)
IngredientKinds.register_kind(CustomKind)
IngredientKinds.register_kind(IndexKind)
