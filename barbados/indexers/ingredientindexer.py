from .baseindexer import BaseIndexer
from barbados.factories import IngredientFactory
from barbados.indexes import IngredientIndex
from barbados.objects.ingredient import Ingredient
from barbados.services.logging import Log
from elasticsearch.exceptions import NotFoundError


class IngredientIndexer(BaseIndexer):

    for_class = Ingredient

    @staticmethod
    def index(ingredient_object):
        index = IngredientFactory.obj_to_index(ingredient_object, IngredientIndex)
        index.save()

    @staticmethod
    def delete(ingredient_object):
        index = IngredientFactory.obj_to_index(ingredient_object, IngredientIndex)
        try:
            IngredientIndex.delete(index)
        except NotFoundError:
            Log.warn("Object %s was not found in index on DELETE. This probably isn't a problem?" % ingredient_object.slug)
