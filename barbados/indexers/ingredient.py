from barbados.indexers.base import BaseIndexer
from barbados.factories.ingredient import IngredientFactory
from barbados.indexes import IngredientIndex
from barbados.objects.ingredient import Ingredient


class IngredientIndexer(BaseIndexer):

    for_class = Ingredient
    for_index = IngredientIndex
    factory = IngredientFactory
