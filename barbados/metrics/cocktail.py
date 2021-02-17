from barbados.metrics import BaseMetric
from barbados.caches.tablescan import CocktailScanCache


class CocktailDrinkCount(BaseMetric):
    key = 'cocktail_drink_count'

    @classmethod
    def collect(cls):
        results = CocktailScanCache.retrieve()
        return len(results)


class CocktailSpecCount(BaseMetric):
    key = 'cocktail_spec_count'

    @classmethod
    def collect(cls):
        count = 0
        results = CocktailScanCache.retrieve()
        for item in results:
            count += len(item.get('specs'))
        return count
