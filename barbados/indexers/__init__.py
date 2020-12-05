from .recipeindexer import RecipeIndexer
from .ingredientindexer import IngredientIndexer
from .menuindexer import MenuIndexer


class IndexerFactory:
    def __init__(self):
        self._indexers = {}
        self._for_indexes = {}

    def register_class(self, indexer):
        for_class = indexer.for_class
        self._indexers[for_class] = indexer

        for_index = indexer.for_index
        self._for_indexes[for_index] = indexer

    def get_indexer(self, indexable):
        """
        Get the Indexer for a particular object
        :param indexable:
        :return:
        """
        class_name = indexable.__class__
        indexer = self._indexers.get(class_name)
        if not indexer:
            raise ValueError(class_name)
        return indexer

    def indexer_for(self, index):
        """
        Get the indexer for a particular index.
        :param index: BarbadosIndex child.
        :return: Indexer.
        """
        indexer = self._for_indexes.get(index)
        if not indexer:
            raise ValueError("Indexer for Index '%s' not found." % index.Index.name)
        return indexer


indexer_factory = IndexerFactory()
indexer_factory.register_class(RecipeIndexer)
indexer_factory.register_class(IngredientIndexer)
indexer_factory.register_class(MenuIndexer)
