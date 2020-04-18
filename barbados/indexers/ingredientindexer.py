from .baseindexer import BaseIndexer
from barbados.factories import IngredientFactory
from barbados.indexes import IngredientIndex
from barbados.caches import IngredientTreeCache
from barbados.objects.ingredient import Ingredient


class IngredientIndexer(BaseIndexer):

    for_class = Ingredient

    @staticmethod
    def index(ingredient_object):
        # ingredient_object.parents = IngredientIndexer._get_parent_slugs(ingredient_object)
        index = IngredientFactory.obj_to_index(ingredient_object, IngredientIndex)
        index.save()

    # @TODO this may not matter, but in bulk-import the tree doesn't exist yet...
    # @staticmethod
    # def _get_parent_slugs(ingredient_object):
    #     ingredient_tree = IngredientTreeCache.retrieve()
    #     parents = ingredient_tree.parents(ingredient_object.slug)
    #     return parents
