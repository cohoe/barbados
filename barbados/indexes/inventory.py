from elasticsearch_dsl import Document, Text, Object
from barbados.indexes.base import BaseIndex, BarbadosIndex


class InventoryIndex(Document, BarbadosIndex):
    id = Text()
    display_name = Text()
    items = Object()
    implicit_items = Object()

    class Index(BaseIndex):
        name = 'inventory'
