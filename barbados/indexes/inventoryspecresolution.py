from elasticsearch_dsl import Document, InnerDoc, Text, Object
from .base import BaseIndex, BarbadosIndex


class ComponentIndex(InnerDoc):
    slug = Text()
    status = Text()
    substitutes = Text(multi=True)
    parent = Text()


class InventorySpecResolution(Document, BarbadosIndex):
    cocktail_slug = Text()
    spec_slug = Text()
    components = Object(ComponentIndex)
    status_count = Object()

    class Index(BaseIndex):
        name = 'inventoryspecresolution'
