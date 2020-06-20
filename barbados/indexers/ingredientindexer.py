from .baseindexer import BaseIndexer
from barbados.factories import IngredientFactory
from barbados.indexes import IngredientIndex
from barbados.objects.ingredient import Ingredient


class IngredientIndexer(BaseIndexer):

    for_class = Ingredient

    @staticmethod
    def index(ingredient_object):
        index = IngredientFactory.obj_to_index(ingredient_object, IngredientIndex)
        index.save()

    @staticmethod
    def delete(ingredient_object):
        index = IngredientFactory.obj_to_index(ingredient_object, IngredientIndex)
        IngredientIndex.delete(index)
