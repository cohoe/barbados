from elasticsearch_dsl import Document, Text
from .base import BaseIndex


class RecipeIndex(Document):
    slug = Text()
    # The whitespace analyzer is needed because alpha can contain '#' which indicates a number
    # and we want to search on that character.
    # https://stackoverflow.com/questions/49322009/elasticsearch-does-not-find-characters-other-than-alpha-numeric
    alpha = Text(analyzer='whitespace', search_analyzer='whitespace')

    class Index(BaseIndex):
        name = 'recipe'
