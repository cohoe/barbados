from barbados.search import SearchBase
from elasticsearch_dsl.query import MatchPhrase, Wildcard
from barbados.indexes import MenuIndex
from barbados.search.occurrences import ShouldOccurrence


class MenuSearch(SearchBase):
    index_class = MenuIndex

    def _build_query_parameters(self):
        self.add_query_parameter(url_parameter='cocktail_slug',
                                 query_class=MatchPhrase,
                                 query_key='query',
                                 fields=['items.cocktail_slug'])

        self.add_query_parameter(url_parameter='name',
                                 query_class=Wildcard,
                                 occurrence=ShouldOccurrence,
                                 fields=['slug', 'display_name'])
