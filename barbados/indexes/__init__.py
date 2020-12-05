from barbados.services.logging import Log
from .recipe import RecipeIndex
from .ingredient import IngredientIndex
from .menu import MenuIndex
from barbados.connectors.elasticsearch import ElasticsearchConnector
from elasticsearch.exceptions import NotFoundError


class IndexFactory:

    def __init__(self):
        self._indexes = {}
        ElasticsearchConnector.connect()

    def register_index(self, index):
        """
        Register an index with this factory. This logs its existence
        and makes it available for things.
        :param index: elasticsearch_dsl.Document child.
        :return: None
        """
        self._indexes[index.Index.name] = index

    def get_index(self, name):
        """
        Get an index class by its name (such as recipe or ingredient).
        :param name: String of the name to lookup.
        :return: elasticsearch_dsl.Document child.
        """
        index = self._indexes.get(name)
        if not index:
            raise ValueError("Index '%s' not found." % name)
        return index

    def init(self):
        """
        Re-initialize all indexes. This calls rebuild on every registered
        index class. There be dragons here.
        :return: None
        """
        for name in self._indexes.keys():
            Log.debug("Init on %s" % name)
            try:
                self.rebuild(self._indexes.get(name))
            except NotFoundError or KeyError or AttributeError as e:
                Log.warning("Error re-initing index %s: %s" % (name, e))

    def rebuild(self, index_class):
        """
        Re-create an index. This deletes the entire index (not just the contents,
        but the Whole Damn Thing(tm). and re-creates it.
        :param index_class: elasticsearch_dsl.Document child representing this index.
        :return: None
        """
        try:
            index_class._index.delete()
            index_class.init()
            Log.info("Successfully rebuilt index %s" % index_class.Index.name)
        except NotFoundError:
            Log.warning("Index %s did not exist." % index_class.Index.name)

    def get_indexes(self):
        """
        Return a dictionary containing all registered ElasticSearch indexes.
        Keys are the name of the index (ex: recipe, ingredient, menu) with the
        value being the class represening that index.
        :return: Dict
        """
        return self._indexes


index_factory = IndexFactory()
index_factory.register_index(RecipeIndex)
index_factory.register_index(IngredientIndex)
index_factory.register_index(MenuIndex)
