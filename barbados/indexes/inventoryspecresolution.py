from elasticsearch_dsl import Document, InnerDoc, Text, Object
from barbados.indexes.base import BaseIndex, BarbadosIndex


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
    # The whitespace analyzer is needed because alpha can contain '#' which indicates a number
    # and we want to search on that character.
    # https://stackoverflow.com/questions/49322009/elasticsearch-does-not-find-characters-other-than-alpha-numeric
    alpha = Text(analyzer='whitespace', search_analyzer='whitespace')

    class Index(BaseIndex):
        name = 'inventoryspecresolution'
