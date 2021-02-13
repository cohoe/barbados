from elasticsearch_dsl import Document, Text, Object, InnerDoc
from barbados.indexes.base import BaseIndex, BarbadosIndex


# class InventoryItemIndex(InnerDoc):
#     parent = Text(analyzer='whitespace', search_analyzer='whitespace')
#     slug = Text(analyzer='whitespace', search_analyzer='whitespace')
#     substitutes = Text(analyzer='whitespace', search_analyzer='whitespace', multi=True)


class InventoryIndex(Document, BarbadosIndex):
    id = Text()
    display_name = Text()
    # These are somewhat of a mess. Disabling until the time comes when it is needed.
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/nested.html
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/flattened.html
    # https://github.com/elastic/elasticsearch-dsl-py/issues/1405
    # items = Object()
    # implicit_items = Object()

    class Index(BaseIndex):
        name = 'inventory'
