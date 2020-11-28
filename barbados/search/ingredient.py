from barbados.search import SearchBase
from elasticsearch_dsl.query import MultiMatch, Match, MatchPhrase
from barbados.indexes import IngredientIndex


class IngredientSearch(SearchBase):
    index_class = IngredientIndex

    def _build_query_parameters(self):
        self.add_query_parameter(url_parameter='name',
                                 query_class=MatchPhrase,
                                 query_key='query',
                                 # type='phrase_prefix',
                                 fields=['slug', 'display_name', 'aliases'])
        self.add_query_parameter(url_parameter='kind',
                                 query_class=Match,
                                 query_key='kind',
                                 fields=['kind'])
