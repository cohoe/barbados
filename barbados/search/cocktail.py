from barbados.search import SearchBase
from elasticsearch_dsl.query import MatchPhrase, Wildcard, Prefix, Match
from barbados.indexes import RecipeIndex


class CocktailSearch(SearchBase):
    index_class = RecipeIndex

    def _build_query_parameters(self):
        self.add_query_parameter(url_parameter='components',
                                 url_parameter_type=list,
                                 query_class=MatchPhrase,
                                 fields=['spec.components.slug', 'spec.components.parents'])
        self.add_query_parameter(url_parameter='name',
                                 query_class=Wildcard,
                                 type='phrase_prefix',
                                 fields=['spec.name', 'display_name'])
        self.add_query_parameter(url_parameter='alpha',
                                 query_class=Prefix,
                                 fields=['alpha'])
        self.add_query_parameter(url_parameter='construction',
                                 query_class=Match,
                                 fields=['spec.construction.slug'])
        self.add_query_parameter(url_parameter='component_count',
                                 query_class=Match,
                                 fields=['spec.component_count'])
        self.add_query_parameter(url_parameter='no_components',
                                 url_parameter_type=list,
                                 query_class=MatchPhrase,
                                 invert=True,
                                 fields=['spec.components.slug', 'spec.component.display_name', 'spec.components.parents'])
