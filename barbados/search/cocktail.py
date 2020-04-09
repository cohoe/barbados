from barbados.search import QueryResult, BaseQuery
from barbados.indexes import RecipeIndex


class CocktailQueryResult(QueryResult):
    """
    Definition of what a query to the cocktail index should return.
    """
    @classmethod
    def _build_query_result(cls, hit):
        return {
            'cocktail_slug': hit.slug,
            'cocktail_display_name': hit.display_name,
            'spec_slug': hit.spec.slug,
            'spec_display_name': hit.spec.display_name,
            'component_display_names': [component['display_name'] for component in hit.spec.components],
        }


class CocktailQuery(BaseQuery):
    """
    Query object representing queries to the Cocktail index.
    """
    def __init__(self, input_parameters, index_class=RecipeIndex, result_class=CocktailQueryResult, name_or_query='bool', sort='_score'):
        super().__init__(index_class, result_class, sort, input_parameters)

        self._build_parameter_field_mappings()
        self._build_query_parameters()

        self.query_config = {
            'name_or_query': name_or_query,
            'must': self._build_query_conditions()
        }

        print(self.query_config)

    # @TODO consolidate these two
    # @TODO there are specialty classes https://github.com/elastic/elasticsearch-dsl-py/blob/2c099d527ed4b17d00b63cd4f49defb9ccea2325/elasticsearch_dsl/query.py
    def _build_parameter_field_mappings(self):
        self.add_parameter_field_mapping('name', ['spec.display_name', 'spec.slug', 'display_name', 'slug'])
        self.add_parameter_field_mapping('components', ['spec.components.slug', 'spec.components.display_name', 'spec.components.parents'])
        self.add_parameter_field_mapping('alpha', ['alpha'])

    def _build_query_parameters(self):
        self.add_query_parameter('name', str)
        self.add_query_parameter('components', list)
        self.add_query_parameter('alpha', str)
