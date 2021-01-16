from elasticsearch_dsl import Document, Text, InnerDoc, Object
from barbados.indexes.base import BaseIndex, BarbadosIndex


class MenuItemIndex(InnerDoc):
    cocktail_slug = Text()
    spec_slug = Text()


class MenuIndex(Document, BarbadosIndex):
    slug = Text()
    display_name = Text()
    items = Object(MenuItemIndex, multi=True)

    class Index(BaseIndex):
        name = 'menu'
