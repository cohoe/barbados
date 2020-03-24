from .baseindexer import BaseIndexer
from barbados.factories import CocktailFactory
from barbados.indexes import RecipeIndex


class RecipeIndexer(BaseIndexer):

    for_class = 'Cocktail'

    @staticmethod
    def index(cocktail_object):
        index = CocktailFactory.obj_to_index(cocktail_object, RecipeIndex)
        index.save()
