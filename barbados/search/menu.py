from barbados.search import SearchBase
from elasticsearch_dsl.query import MultiMatch, Match, MatchPhrase
from barbados.indexes import MenuIndex


class MenuSearch(SearchBase):
    index_class = MenuIndex

    def _build_query_parameters(self):
        self.add_query_parameter(url_parameter='cocktail_slug',
                                 query_class=MatchPhrase,
                                 query_key='query',
                                 # type='phrase_prefix',
                                 fields=['items.cocktail_slug'])
