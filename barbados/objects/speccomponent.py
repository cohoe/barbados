from barbados.objects.caches import IngredientTreeCache


class SpecComponent:
    """
    Someday the direct name part might be able to go away.
    """

    # This defines nodes in the IngredientTree that should be excluded
    # from the count.
    # @TODO move this to zookeeper config
    ingredient_count_excludes = ['bitters']

    def __init__(self, slug, display_name, quantity=None, unit=None):
        self.slug = slug
        self.display_name = display_name
        self.quantity = quantity
        self.unit = unit
        self.countable = True

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
