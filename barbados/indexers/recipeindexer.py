from .baseindexer import BaseIndexer
from barbados.factories import CocktailFactory
from barbados.indexes import RecipeIndex
from barbados.objects.cocktail import Cocktail


class RecipeIndexer(BaseIndexer):

    for_class = Cocktail

    @staticmethod
    def index(cocktail_object):
        indexables = CocktailFactory.obj_to_index(cocktail_object, RecipeIndex)
        [indexable.save() for indexable in indexables]
