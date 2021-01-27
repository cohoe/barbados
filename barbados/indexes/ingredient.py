from elasticsearch_dsl import Document, Text
from barbados.indexes.base import BaseIndex, BarbadosIndex


class IngredientIndex(Document, BarbadosIndex):
    slug = Text(analyzer='whitespace', search_analyzer='whitespace')
    display_name = Text()
    parent = Text(analyzer='whitespace', search_analyzer='whitespace')
    parents = Text(analyzer='whitespace', search_analyzer='whitespace', multi=True)
    aliases = Text()

    class Index(BaseIndex):
        name = 'ingredient'
