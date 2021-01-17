from elasticsearch_dsl import Document, Text, InnerDoc, Object
from barbados.indexes.base import BaseIndex, BarbadosIndex


class DrinkListItemIndex(InnerDoc):
    cocktail_slug = Text()
    spec_slug = Text()


class DrinkListIndex(Document, BarbadosIndex):
    id = Text()
    display_name = Text()
    items = Object(DrinkListItemIndex, multi=True)

    class Index(BaseIndex):
        name = 'drinklist'
