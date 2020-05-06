from barbados.services.logging import Log
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
            Log.debug("Init on %s" % name)
            try:
                self._indexes[name]._index.delete()
            except NotFoundError:
                pass
            self._indexes[name].init()

    def rebuild(self, index_class):
        try:
            index_class._index.delete()
            index_class.init()
            Log.info("Successfully rebuilt index %s" % index_class.Index.name)
        except NotFoundError:
            Log.warning("Index %s did not exist." % index_class.Index.name)


index_factory = IndexFactory()
index_factory.register_index(RecipeIndex)
index_factory.register_index(IngredientIndex)
