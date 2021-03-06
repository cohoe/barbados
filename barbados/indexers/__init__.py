from barbados.indexers.recipe import RecipeIndexer
from barbados.indexers.ingredient import IngredientIndexer
from barbados.indexers.drinklist import DrinkListIndexer
from barbados.indexers.inventoryspec import InventorySpecResolutionIndexer


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


indexer_factory = IndexerFactory()
indexer_factory.register_class(RecipeIndexer)
indexer_factory.register_class(IngredientIndexer)
indexer_factory.register_class(DrinkListIndexer)
indexer_factory.register_class(InventorySpecResolutionIndexer)


class ObjectIndexer:
    """
    Generic object indexer class that provides a common way to index
    any supported object.
    """
    @staticmethod
    def index(indexable):
        """
        Take an object and index it.
        :param indexable: barbados.objects.* that supports indexation.
        @TODO someday should indexes return the index object for what they made?
        """
        indexer = indexer_factory.get_indexer(indexable=indexable)
        indexer.index(indexable)
