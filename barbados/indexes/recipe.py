from elasticsearch_dsl import Document, InnerDoc, Text, Integer, Object, Keyword
from barbados.indexes.base import BaseIndex, BarbadosIndex
from barbados.objects.cocktail import Cocktail


# https://github.com/elastic/elasticsearch-dsl-py/blob/master/examples/parent_child.py
# https://github.com/elastic/elasticsearch-dsl-py/issues/637


class NoteIndex(InnerDoc):
    text = Text()


class GarnishIndex(InnerDoc):
    slug = Text(analyzer='whitespace', search_analyzer='whitespace')
    display_name = Text()
    notes = Object(NoteIndex, multi=True)


class ComponentIndex(InnerDoc):
    slug = Text(analyzer='whitespace', search_analyzer='whitespace')
    display_name = Text(analyzer='whitespace', search_analyzer='whitespace')
    quantity = Integer()
    unit = Text()
    parents = Text(multi=True)


class SpecIndex(InnerDoc):
    garnish = Object(GarnishIndex)
    components = Object(ComponentIndex)


class RecipeIndex(Document, BarbadosIndex):
    # The whitespace analyzer is needed because alpha can contain '#' which indicates a number
    # and we want to search on that character. Same thing with slugs and '-''s.
    # https://stackoverflow.com/questions/49322009/elasticsearch-does-not-find-characters-other-than-alpha-numeric
    slug = Text(analyzer='whitespace', search_analyzer='whitespace')
    alpha = Text(analyzer='whitespace', search_analyzer='whitespace')
    spec = Object(SpecIndex)

    class Index(BaseIndex):
        name = 'recipe'
