from barbados.metrics import BaseMetric
from barbados.caches.ingredienttree import IngredientTreeCache


class IngredientAllCount(BaseMetric):
    key = 'ingredient_all_count'

    @classmethod
    def collect(cls):
        tree = IngredientTreeCache.retrieve()
        return len(tree)
