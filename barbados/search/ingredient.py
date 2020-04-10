from barbados.search import SearchResults, SearchBase
from elasticsearch_dsl.query import MultiMatch, Prefix, Match
from barbados.indexes import IngredientIndex


class IngredientSearchResults(SearchResults):
    """
    Definition of what a query to the ingredient index should return.
    """

    @classmethod
    def _serialize_hit(cls, hit):
        return {
            'slug': hit.slug,
            'display_name': hit.display_name,
            'kind': hit.kind,
            'aliases': hit.aliases,
        }


class IngredientSearch(SearchBase):
    index_class = IngredientIndex
    result_class = IngredientSearchResults

    def _build_query_parameters(self):
        self.add_query_parameter(parameter='name', query_class=MultiMatch, query_key='query', type='phrase_prefix',
                                 fields=['slug', 'display_name', 'aliases'])
        self.add_query_parameter(parameter='kind', query_class=Match, query_key='kind')
