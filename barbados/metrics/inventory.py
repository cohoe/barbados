from barbados.metrics import BaseMetric
from barbados.search.reciperesolution import RecipeResolutionSearch
from barbados.metrics.cocktail import CocktailSpecCount


class InventoryMetric(BaseMetric):
    def __init__(self, inventory):
        self.inventory = inventory
        # I'm not sure it's appropriate to reference self.instnace in the search queries below.
        # Particularly if that ever changes.
        self.instance = str(inventory.id)

    def collect(self):
        raise NotImplementedError


class InventoryItemsDirectCount(InventoryMetric):
    key = 'inventory_items_direct_count'

    def collect(self):
        return len(self.inventory.items)


class InventoryItemsImplicitCount(InventoryMetric):
    key = 'inventory_items_implicit_count'

    def collect(self):
        return len(self.inventory.implicit_items)


class InventoryResolutionMissingNoneCount(InventoryMetric):
    key = 'inventory_resolution_missing_none_count'

    def collect(self):
        results = RecipeResolutionSearch(inventory_id=str(self.inventory.id), missing=0).execute()
        return len(results)


class InventoryResolutionMissingOneCount(InventoryMetric):
    key = 'inventory_resolution_missing_one_count'

    def collect(self):
        results = RecipeResolutionSearch(inventory_id=str(self.inventory.id), missing=1).execute()
        return len(results)


class InventoryResolutionMissingTwoPlusCount(InventoryMetric):
    key = 'inventory_resolution_missing_twoplus_count'

    def collect(self):
        results = RecipeResolutionSearch(inventory_id=str(self.inventory.id), missing='2+').execute()
        return len(results)


class InventoryResolutionMissingAnyCount(InventoryMetric):
    key = 'inventory_resolution_missing_any_count'

    def collect(self):
        results = RecipeResolutionSearch(inventory_id=str(self.inventory.id), missing='1+').execute()
        return len(results)


class InventoryResolutionAvailableRecipePercent(InventoryMetric):
    key = 'inventory_resolution_available_recipe_percent'

    def collect(self):
        results = RecipeResolutionSearch(inventory_id=str(self.inventory.id), missing=0).execute()
        total = CocktailSpecCount.collect()

        return round((len(results) / total)*100, 2)
