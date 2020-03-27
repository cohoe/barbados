from barbados.objects.slug import Slug
from barbados.objects.displayname import DisplayName
from barbados.objects.caches import IngredientTreeCache


class SpecComponent:
    """
    Someday the direct name part might be able to go away.
    """

    # This defines nodes in the IngredientTree that should be excluded
    # from the count.
    ingredient_count_excludes = ['bitters']

    def __init__(self, name, quantity=None, unit=None, display_name=None, slug=None):
        self.name = name
        self.slug = slug
        self.display_name = display_name
        self.quantity = quantity
        self.unit = unit
        self.countable = True

        if self.slug is None:
            self.slug = Slug(name)
        if self.display_name is None:
            self.display_name = DisplayName(name)

        ingredient_tree = IngredientTreeCache.retrieve()
        self.parents = ingredient_tree.parents(self.slug)

        if self.slug in self.ingredient_count_excludes:
            self.countable = False
        else:
            for parent in self.parents:
                if parent in self.ingredient_count_excludes:
                    self.countable = False
                    break

    def __repr__(self):
        return "Barbados::Objects::SpecComponent[%s]" % self.slug

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('display_name', self.display_name)
        serializer.add_property('quantity', self.quantity)
        serializer.add_property('unit', self.unit)
        serializer.add_property('parents', self.parents)
