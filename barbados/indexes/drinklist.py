from elasticsearch_dsl import Document, Text, InnerDoc, Object
from barbados.indexes.base import BaseIndex, BarbadosIndex


class DrinkListItemIndex(InnerDoc):
    cocktail_slug = Text(analyzer='whitespace', search_analyzer='whitespace')
    spec_slug = Text(analyzer='whitespace', search_analyzer='whitespace')


class DrinkListIndex(Document, BarbadosIndex):
    id = Text(analyzer='whitespace', search_analyzer='whitespace')
    display_name = Text()
    items = Object(DrinkListItemIndex, multi=True)

    class Index(BaseIndex):
        name = 'drinklist'
