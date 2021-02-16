import numpy
from barbados.metrics import BaseMetric
from barbados.search.reciperesolution import RecipeResolutionSearch
from barbados.metrics.cocktail import CocktailSpecCount
from barbados.factories.reciperesolution import RecipeResolutionFactory
from barbados.objects.resolution.status import MissingResolutionStatus, DirectResolutionStatus


class InventoryMetric(BaseMetric):
    def __init__(self, inventory):
        self.inventory = inventory
        # I'm not sure it's appropriate to reference self.instnace in the search queries below.
        # Particularly if that ever changes.
        self.instance = str(inventory.id)

    def collect(self):
        raise NotImplementedError

    @staticmethod
    def get_status_dict_from_results(results, status):
        components = []

        # Build the RecipeResolutionSummary objects based on each search result.
        for result in results:
            rs = RecipeResolutionFactory.raw_to_obj(result.get('hit'))
            components += rs.get_components_by_status(status)

        # Calculate the unique values from the results and how many of each there were.
        # https://stackoverflow.com/questions/12282232/how-do-i-count-unique-values-inside-a-list
        values, counts = numpy.unique(components, return_counts=True)
        # Build a dictionary from the two arrays.
        # https://www.geeksforgeeks.org/python-convert-two-lists-into-a-dictionary/
        status_counts = {values[i]: counts[i] for i in range(len(values))}
        # Sort the keys into a meaningful order. The first directive creates a list of tuples.
        # The second puts the back into a dictionary.
        # https://careerkarma.com/blog/python-sort-a-dictionary-by-value/
        sorted_counts = sorted(status_counts.items(), key=lambda x: x[1], reverse=True)
        new_status_counts = {i[0]: int(i[1]) for i in sorted_counts}

        return new_status_counts


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


class InventoryResolutionMissingLeaderboard(InventoryMetric):
    key = 'inventory_resolution_missing_leaderboard'

    def collect(self):
        results = RecipeResolutionSearch(inventory_id=str(self.inventory.id), missing='1+').execute()
        return self.get_status_dict_from_results(results, MissingResolutionStatus)


class InventoryResolutionDirectLeaderboard(InventoryMetric):
    key = 'inventory_resolution_direct_leaderboard'

    def collect(self):
        results = RecipeResolutionSearch(inventory_id=str(self.inventory.id), missing='0').execute()
        return self.get_status_dict_from_results(results, DirectResolutionStatus)
