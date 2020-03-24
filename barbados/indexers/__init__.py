from .recipeindexer import RecipeIndexer


class IndexerFactory:
    def __init__(self):
        self._indexers = {}

    def register_class(self, indexer):
        for_class = indexer.for_class
        self._indexers[for_class] = indexer

    def get_indexer(self, indexable):
        class_name = indexable.__class__.__name__
        indexer = self._indexers.get(class_name)
        if not indexer:
            raise ValueError(class_name)
        return indexer


indexer_factory = IndexerFactory()
indexer_factory.register_class(RecipeIndexer)
