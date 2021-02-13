from barbados.indexers.base import BaseIndexer
from barbados.factories.reciperesolution import RecipeResolutionFactory
from barbados.indexes import InventorySpecResolutionIndex
from barbados.objects.resolution.summary import RecipeResolutionSummary


class InventorySpecResolutionIndexer(BaseIndexer):

    for_class = RecipeResolutionSummary
    for_index = InventorySpecResolutionIndex
    factory = RecipeResolutionFactory
