from barbados.indexers.base import BaseIndexer
from barbados.factories.specresolution import SpecResolutionFactory
from barbados.indexes import InventorySpecResolution
from barbados.resolution.summary import SpecResolutionSummary


class InventorySpecResolutionIndexer(BaseIndexer):

    for_class = SpecResolutionSummary
    for_index = InventorySpecResolution
    factory = SpecResolutionFactory
