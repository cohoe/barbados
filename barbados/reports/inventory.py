from barbados.reports import BaseReport
from barbados.objects.resolution.status import MissingResolutionStatus, DirectResolutionStatus
from barbados.search.reciperesolution import RecipeResolutionSearch
from barbados.caches.ingredienttree import IngredientTreeCache


class InventoryReport(BaseReport):
    def __init__(self, inventory):
        self.inventory = inventory

    def run(self):
        total = RecipeResolutionSearch().execute()
        missing_0 = RecipeResolutionSearch(missing=0).execute()
        missing_1 = RecipeResolutionSearch(missing=1).execute()
        missing_2plus = RecipeResolutionSearch(missing='2+').execute()

        missing_any = missing_1 + missing_2plus

        missing_counts = self.get_status_dict_from_results(missing_any, MissingResolutionStatus)
        direct_counts = self.get_status_dict_from_results(missing_0, DirectResolutionStatus)

        tree = IngredientTreeCache.retrieve()
        self.inventory.expand(tree)

        # @TODO should report list all drink names or slugs?
        # @TODO add datetime generated
        # @TODO use the word tally
        # @TODO give percentage of what you can make
        report = {
            'inventory_id': str(self.inventory.id),
            'supported_ingredients': len(tree),
            'items_direct': len(self.inventory.items),
            'items_indirect': len(self.inventory.implicit_items),
            'count_total_recipes': len(total),
            'count_missing_0': len(missing_0),
            'count_missing_1': len(missing_1),
            'count_missing_2+': len(missing_2plus),
            'count_missing_any': len(missing_any),
            'missing_component_tally': missing_counts,
            'direct_component_tally': direct_counts,
        }

        return report
