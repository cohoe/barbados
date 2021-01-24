from barbados.objects.base import BaseObject
from barbados.objects.ingredientkinds import IngredientKinds, IndexKind
from barbados.query import QueryBuilder
from barbados.models.ingredient import IngredientModel
from barbados.serializers import ObjectSerializer
from datetime import datetime


class Ingredient(BaseObject):
    def __init__(self, slug, display_name, kind, parent=None, aliases=None, elements=None,
                 conditions=None, elements_include=None, elements_exclude=None, last_refresh=None):
        """
        Ingredient
        :param slug: Slug ID of this ingredient.
        :param display_name: DisplayName of the ingredient.
        :param kind: IngredientKind object.
        :param parent: Slug of the parent of this ingredient.
        :param aliases: List of DisplayName strings.
        :param elements: List of Ingredient slugs that are part of this index.
        :param conditions: List of QueryCondition objects that generate elements for this index.
        :param elements_include: List of Ingredient slugs that should be manually included in this index.
        :param elements_exclude: List of Ingredient slugs that should be excluded from this index.
        :param last_refresh: Datetime of the last refresh of the elements in this index.
        """
        if aliases is None:
            aliases = []

        if elements is None:
            elements = []

        if conditions is None:
            conditions = []

        if elements_exclude is None:
            elements_exclude = []

        if elements_include is None:
            elements_include = []

        self.slug = slug
        self.display_name = display_name
        self.kind = IngredientKinds(kind)
        self.parent = parent
        self.aliases = aliases
        self.elements = elements
        self.conditions = conditions
        self.elements_include = elements_include
        self.elements_exclude = elements_exclude
        self.last_refresh = last_refresh

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('display_name', self.display_name)
        serializer.add_property('kind', self.kind.value)
        serializer.add_property('parent', self.parent)
        serializer.add_property('aliases', self.aliases)
        serializer.add_property('elements', self.elements)
        serializer.add_property('conditions', [ObjectSerializer.serialize(condition, serializer.format) for condition in self.conditions])
        serializer.add_property('elements_include', self.elements_include)
        serializer.add_property('elements_exclude', self.elements_exclude)
        serializer.add_property('last_refresh', self.last_refresh)

    def refresh(self, session):
        """
        If this ingredient is an index, its elements can be refreshed
        from the current ingredient dataset based on conditions and
        explicit include/exclude lists.
        :return: None
        """
        if self.kind is not IndexKind:
            raise Exception("Refresh is not supported for %s" % self.kind)

        results = QueryBuilder(model=IngredientModel, conditions=self.conditions).execute(session=session)
        self.elements = [result.slug for result in results]

        # Add the includes and remove the excludes
        self.elements += self.elements_include
        for exclude in self.elements_exclude:
            try:
                self.elements.remove(exclude)
            except ValueError:
                pass

        # dedup the list
        self.elements = list(set(self.elements))

        # Update the last_refresh time to now so we know when it was last done.
        self.last_refresh = datetime.utcnow()
