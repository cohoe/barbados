import logging
from .recipe import RecipeIndex
from .ingredient import IngredientIndex
from barbados.connectors.elasticsearch import ElasticsearchConnector
from elasticsearch.exceptions import NotFoundError


class IndexFactory:

    def __init__(self):
        self._indexes = {}
        ElasticsearchConnector.connect()

    def register_index(self, index):
        self._indexes[index.Index.name] = index

    def get_index(self, name):
        index = self._indexes.get(name)
        if not index:
            raise ValueError(index)
        return index

    def init(self):
        for name in self._indexes.keys():
            logging.debug("Init on %s" % name)
            try:
                self._indexes[name]._index.delete()
            except NotFoundError:
                pass
            self._indexes[name].init()


index_factory = IndexFactory()
index_factory.register_index(RecipeIndex)
index_factory.register_index(IngredientIndex)
