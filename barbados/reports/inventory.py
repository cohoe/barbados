import barbados.metrics.ingredient
import barbados.metrics.inventory
import barbados.metrics.cocktail
from barbados.reports import BaseReport
from barbados.caches.ingredienttree import IngredientTreeCache
from barbados.objects.text import Timestamp


class InventoryReport(BaseReport):
    def __init__(self, inventory):
        self.inventory = inventory
        self.metrics = [
            barbados.metrics.ingredient.IngredientAllCount,
            barbados.metrics.inventory.InventoryItemsDirectCount(self.inventory),
            barbados.metrics.inventory.InventoryItemsImplicitCount(self.inventory),
            barbados.metrics.cocktail.CocktailDrinkCount,
            barbados.metrics.cocktail.CocktailSpecCount,
            barbados.metrics.inventory.InventoryResolutionMissingNoneCount(self.inventory),
            barbados.metrics.inventory.InventoryResolutionMissingOneCount(self.inventory),
            barbados.metrics.inventory.InventoryResolutionMissingTwoPlusCount(self.inventory),
            barbados.metrics.inventory.InventoryResolutionMissingAnyCount(self.inventory),
            barbados.metrics.inventory.InventoryResolutionAvailableRecipePercent(self.inventory),
            barbados.metrics.inventory.InventoryResolutionMissingLeaderboard(self.inventory),
            barbados.metrics.inventory.InventoryResolutionDirectLeaderboard(self.inventory)
        ]

    def run(self):
        tree = IngredientTreeCache.retrieve()
        self.inventory.expand(tree)

        report = {
            'inventory_id': str(self.inventory.id),
            'generated_at': Timestamp()
        }

        [report.update({metric.key: metric.collect()}) for metric in self.metrics]

        return report
