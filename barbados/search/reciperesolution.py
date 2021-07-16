from barbados.search import SearchBase
from elasticsearch_dsl.query import MatchPhrase, Wildcard, Prefix, Match, Range, Exists, MultiMatch
from barbados.indexes.reciperesolutionindex import RecipeResolutionIndex
from barbados.search.occurrences import ShouldOccurrence


class RecipeResolutionSearch(SearchBase):
    index_class = RecipeResolutionIndex

    def _build_query_parameters(self):
        self.add_query_parameter(url_parameter='inventory_id',
                                 query_class=Match,
                                 fields=['inventory_id'])
        self.add_query_parameter(url_parameter='missing',
                                 query_class=Range,
                                 url_parameter_type=dict,
                                 value_parser=self._parse_range_value,
                                 fields=['status_count.MISSING'])
        # These are all the same as the CocktailSearch, just with different fields.
        self.add_query_parameter(url_parameter='components',
                                 url_parameter_type=list,
                                 query_class=MatchPhrase,
                                 fields=['components.slug', 'components.parents'])
        self.add_query_parameter(url_parameter='no_components',
                                 url_parameter_type=list,
                                 query_class=MatchPhrase,
                                 invert=True,
                                 fields=['components.slug', 'components.parents'])
        self.add_query_parameter(url_parameter='name',
                                 query_class=Wildcard,
                                 occurrence=ShouldOccurrence,
                                 fields=['cocktail_slug', 'spec_slug'])
        self.add_query_parameter(url_parameter='alpha',
                                 query_class=Prefix,
                                 fields=['alpha'])
        self.add_query_parameter(url_parameter='construction',
                                 query_class=Match,
                                 fields=['construction_slug'])
        self.add_query_parameter(url_parameter='component_count',
                                 query_class=Range,
                                 url_parameter_type=dict,
                                 value_parser=self._parse_range_value,
                                 fields=['component_count'])
        self.add_query_parameter(url_parameter='garnish',
                                 url_parameter_type=bool,
                                 query_class=Exists,
                                 fields=['garnish'])
        self.add_query_parameter(url_parameter='citation_name',
                                 query_class=MatchPhrase,
                                 occurrence=ShouldOccurrence,
                                 fields=['citations.publisher', 'citations.title'])
        self.add_query_parameter(url_parameter='citation_author',
                                 query_class=MatchPhrase,
                                 fields=['citations.author'])
        self.add_query_parameter(url_parameter='all',
                                 query_class=MultiMatch,
                                 fields=['*'])
