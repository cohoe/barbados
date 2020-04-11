from barbados.search import SearchBase
from elasticsearch_dsl.query import MultiMatch, Prefix
from barbados.indexes import RecipeIndex


class CocktailSearch(SearchBase):
    index_class = RecipeIndex

    def _build_query_parameters(self):
        self.add_query_parameter(parameter='components', query_class=MultiMatch, query_key='query', type='phrase_prefix',
                                 fields=['spec.components.slug', 'specs.component.display_name', 'spec.components.parents'])
        self.add_query_parameter(parameter='name', query_class=MultiMatch, query_key='query', type='phrase_prefix',
                                 fields=['spec.name', 'display_name'])
        self.add_query_parameter(parameter='alpha', query_class=Prefix, query_key='alpha')
