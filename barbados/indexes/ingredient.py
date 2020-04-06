from elasticsearch_dsl import Document, Text
from .base import BaseIndex


class IngredientIndex(Document):
    slug = Text()
    display_name = Text()
    parent = Text()
    parents = Text()

    class Index(BaseIndex):
        name = 'ingredient'
