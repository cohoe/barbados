from elasticsearch_dsl import Document, Text, InnerDoc, Object
from barbados.indexes.base import BaseIndex, BarbadosIndex


class ListItemIndex(InnerDoc):
    cocktail_slug = Text(analyzer='whitespace', search_analyzer='whitespace')
    spec_slug = Text(analyzer='whitespace', search_analyzer='whitespace')


class ListIndex(Document, BarbadosIndex):
    id = Text(analyzer='whitespace', search_analyzer='whitespace')
    display_name = Text()
    items = Object(ListItemIndex, multi=True)

    class Index(BaseIndex):
        name = 'list'
