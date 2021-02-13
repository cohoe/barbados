from barbados.indexers.base import BaseIndexer
from barbados.factories.reciperesolution import RecipeResolutionFactory
from barbados.indexes import RecipeResolutionIndex
from barbados.objects.resolution.summary import RecipeResolutionSummary


class RecipeResolutionIndexer(BaseIndexer):

    for_class = RecipeResolutionSummary
    for_index = RecipeResolutionIndex
    factory = RecipeResolutionFactory
