from barbados.indexers.base import BaseIndexer
from barbados.factories.ingredientfactory import IngredientFactory
from barbados.indexes import IngredientIndex
from barbados.objects.ingredient import Ingredient
from barbados.services.logging import LogService
from elasticsearch.exceptions import NotFoundError


class IngredientIndexer(BaseIndexer):

    for_class = Ingredient
    for_index = IngredientIndex
    factory = IngredientFactory

    @classmethod
    def index(cls, ingredient_object):
        index = IngredientFactory.obj_to_index(ingredient_object, cls.for_index)
        index.save()

    @classmethod
    def delete(cls, ingredient_object):
        index = IngredientFactory.obj_to_index(ingredient_object, cls.for_index)
        try:
            IngredientIndex.delete(index)
        except NotFoundError:
            LogService.warn("Object %s was not found in index on DELETE. This probably isn't a problem?" % ingredient_object.slug)
