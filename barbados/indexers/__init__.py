from barbados.indexers.recipe import RecipeIndexer
from barbados.indexers.ingredient import IngredientIndexer
from barbados.indexers.drinklist import DrinkListIndexer
from barbados.indexers.inventoryspec import InventorySpecResolutionIndexer
from barbados.indexers.inventory import InventoryIndexer


class IndexerFactory:
    """
    This factory controls loading of all indexers and can provide them to consumers
    based on a number of factors.
    """
    def __init__(self):
        """
        The internal tracking data should not be exposed publicly.
        """
        self._indexers = {}
        self._for_indexes = {}

    def register_class(self, indexer):
        """
        Load an indexer into this system for use.
        :param indexer: Child class of barbados.indexers.base.BaseIndexer.
        :return: None
        """
        for_class = indexer.for_class
        self._indexers[for_class] = indexer

        for_index = indexer.for_index
        self._for_indexes[for_index] = indexer

    def get_indexer(self, indexable):
        """
        Get the Indexer for a particular object.
        :param indexable: Object of any type that should be indexable.
        :return: Child class of barbados.indexers.base.BaseIndexer that can be used to index the object.
        """
        class_name = indexable.__class__
        indexer = self._indexers.get(class_name)
        if not indexer:
            raise ValueError(class_name)
        return indexer

    def indexer_for(self, index):
        """
        Get the indexer for a particular index.
        :param index: barbados.indexes.base.BaseIndex child representing an ElasticSearch index.
        :return: Child class of barbados.indexers.base.BaseIndexer that can be used to index to the Index.
        """
        indexer = self._for_indexes.get(index)
        if not indexer:
            raise ValueError("Indexer for Index '%s' not found." % index.Index.name)
        return indexer


Indexers = IndexerFactory()
Indexers.register_class(RecipeIndexer)
Indexers.register_class(IngredientIndexer)
Indexers.register_class(DrinkListIndexer)
Indexers.register_class(InventorySpecResolutionIndexer)
Indexers.register_class(InventoryIndexer)
