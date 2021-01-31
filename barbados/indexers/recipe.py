from barbados.indexers.base import BaseIndexer
from barbados.factories.cocktailfactory import CocktailFactory
from barbados.indexes import RecipeIndex
from barbados.objects.cocktail import Cocktail
from elasticsearch.exceptions import NotFoundError
from barbados.services.logging import LogService


class RecipeIndexer(BaseIndexer):

    for_class = Cocktail
    for_index = RecipeIndex
    factory = CocktailFactory

    @staticmethod
    def index(cocktail_object):
        indexables = CocktailFactory.obj_to_index(cocktail_object, RecipeIndex)
        [indexable.save() for indexable in indexables]

    @staticmethod
    def delete(cocktail_object):
        try:
            indexables = CocktailFactory.obj_to_index(cocktail_object, RecipeIndex)
            for indexable in indexables:
                try:
                    RecipeIndex.delete(indexable)
                except NotFoundError:
                    LogService.warning("No cache entry found for %s" % indexable)
        except KeyError as e:
            # Since this is a DELETE situation we don't particularly care to correct
            # the problem, but if we're creating or some other thing that could be
            # more problematic.
            LogService.error("Recipe has bad data: %s" % e)
