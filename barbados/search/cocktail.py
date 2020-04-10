from barbados.search import SearchResults, SearchBase
from elasticsearch_dsl.query import MultiMatch, Prefix
from barbados.indexes import RecipeIndex


class CocktailSearchResults(SearchResults):
    """
    Definition of what a query to the cocktail index should return.
    """

    @classmethod
    def _serialize_hit(cls, hit):
        return {
            'cocktail_slug': hit.slug,
            'cocktail_display_name': hit.display_name,
            'spec_slug': hit.spec.slug,
            'spec_display_name': hit.spec.display_name,
            'component_display_names': [component['display_name'] for component in hit.spec.components],
        }


class CocktailSearch(SearchBase):
    index_class = RecipeIndex
    result_class = CocktailSearchResults

    def _build_query_parameters(self):
        self.add_query_parameter(parameter='components', query_class=MultiMatch, query_key='query', type='phrase_prefix',
                                 fields=['spec.components.slug', 'specs.component.display_name', 'spec.components.parents'])
        self.add_query_parameter(parameter='name', query_class=MultiMatch, query_key='query', type='phrase_prefix',
                                 fields=['spec.name', 'display_name'])
        self.add_query_parameter(parameter='alpha', query_class=Prefix, query_key='alpha')
