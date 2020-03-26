from barbados.objects.caches import IngredientTreeCache
from barbados.objects.slug import Slug


class SpecIngredient:
    def __init__(self, name, quantity=None, unit=None, include_parents=True):
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.slug = Slug(name)

        # @TODO this may break some stuff. Perhaps garnish should be its own
        # object type?
        if include_parents:
            ingredient_tree = IngredientTreeCache.retrieve()
            self.parents = ingredient_tree.parents(self.slug)
        else:
            self.parents = []

        if isinstance(self.name, str):
            if len(self.name) <= 1:
                raise KeyError("Got single character or less for name. Probably a data problem. Got '%s'" % self.name)

    def __repr__(self):
        return "<Object:SpecIngredient::name=%s>" % self.name

    def serialize(self):
        keys = ['name', 'quantity', 'unit', 'parents']
        ser = {}
        for key in keys:
            if getattr(self, key) is not None:
                ser[key] = getattr(self, key)
        return ser

    # Old code for doing pretty quantity conversion:
    #
    # if type(quantity) == float:
    #     for fraction in pretty_fractions:
    #         quantity = str(quantity).replace(fraction, pretty_fractions[fraction])
    #     quantity = quantity.lstrip('0')
    #     ingredient['quantity'] = quantity
