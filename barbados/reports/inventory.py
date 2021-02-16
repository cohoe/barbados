import barbados.metrics.ingredient
import barbados.metrics.inventory
import barbados.metrics.cocktail
from barbados.reports import BaseReport
from barbados.objects.resolution.status import MissingResolutionStatus, DirectResolutionStatus
from barbados.search.reciperesolution import RecipeResolutionSearch
from barbados.caches.ingredienttree import IngredientTreeCache
from barbados.objects.text import Timestamp


class InventoryReport(BaseReport):
    def __init__(self, inventory):
        self.inventory = inventory

    def run(self):
        total = RecipeResolutionSearch(inventory_id=str(self.inventory.id)).execute()
        missing_0 = RecipeResolutionSearch(inventory_id=str(self.inventory.id), missing=0).execute()
        missing_1 = RecipeResolutionSearch(inventory_id=str(self.inventory.id), missing=1).execute()
        missing_2plus = RecipeResolutionSearch(inventory_id=str(self.inventory.id), missing='2+').execute()

        missing_any = missing_1 + missing_2plus

        missing_counts = self.get_status_dict_from_results(missing_any, MissingResolutionStatus)
        direct_counts = self.get_status_dict_from_results(missing_0, DirectResolutionStatus)

        tree = IngredientTreeCache.retrieve()
        self.inventory.expand(tree)

        # @TODO should report list all drink names or slugs?
        report = {
            'inventory_id': str(self.inventory.id),
            'supported_ingredients': barbados.metrics.ingredient.IngredientAllCount.collect(),
            'items_direct': barbados.metrics.inventory.InventoryItemsDirectCount(self.inventory).collect(),
            'items_indirect': barbados.metrics.inventory.InventoryItemsImplicitCount(self.inventory).collect(),
            'count_total_drinks': barbados.metrics.cocktail.CocktailDrinkCount.collect(),
            'count_total_recipes': barbados.metrics.cocktail.CocktailSpecCount.collect(),
            'count_missing_0': barbados.metrics.inventory.InventoryResolutionMissingNoneCount(self.inventory).collect(),
            'count_missing_1': barbados.metrics.inventory.InventoryResolutionMissingOneCount(self.inventory).collect(),
            'count_missing_2+': barbados.metrics.inventory.InventoryResolutionMissingTwoPlusCount(self.inventory).collect(),
            'count_missing_any': barbados.metrics.inventory.InventoryResolutionMissingAnyCount(self.inventory).collect(),
            'percent_recipe_available': barbados.metrics.inventory.InventoryResolutionAvailableRecipePercent(self.inventory).collect(),
            'missing_component_tally': missing_counts,
            'direct_component_tally': direct_counts,
            'generated_at': Timestamp()
        }

        return report
