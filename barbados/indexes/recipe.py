from elasticsearch_dsl import Document, Text
from .base import BaseIndex


class RecipeIndex(Document):
    slug = Text()

    class Index(BaseIndex):
        name = 'recipe'
