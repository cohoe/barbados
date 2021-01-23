from barbados.objects.base import BaseObject
from barbados.objects.ingredientkinds import IngredientKinds, IndexKind
from barbados.query import QueryCondition, QueryBuilder
from barbados.models.ingredient import IngredientModel


class Ingredient(BaseObject):
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

    def refresh(self, session):
        """
        If this ingredient is an index, its elements can be refreshed
        from the current ingredient dataset.
        :return: None
        """
        if self.kind is not IndexKind:
            raise Exception("Refresh is not supported for %s" % self.kind)

        conditions = [
            QueryCondition(bin_op='or', field='slug', operator='contains', value='el-dorado'),
            QueryCondition(bin_op='or', field='slug', operator='contains', value='appleton')
        ]

        results = QueryBuilder(model=IngredientModel, conditions=conditions).execute(session=session)
        self.elements = [result.slug for result in results]
