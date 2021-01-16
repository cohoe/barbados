from elasticsearch_dsl import Document, Text
from barbados.indexes.base import BaseIndex, BarbadosIndex


class IngredientIndex(Document, BarbadosIndex):
    slug = Text()
    display_name = Text()
    parent = Text()
    parents = Text()
    aliases = Text()

    class Index(BaseIndex):
        name = 'ingredient'
