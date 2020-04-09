import logging
from barbados.indexes import RecipeIndex


class QueryParameter:
    def __new__(cls, query, fields, kind='multi_match', type_='phrase_prefix'):
        return {
            kind: {
                'query': query,
                'type': type_,
                'fields': fields,
            }
        }


class QueryResult:
    def __new__(cls, hit):
        return {
            'id': hit.meta.id,
            'score': hit.meta.score,
            'result': cls._build_query_result(hit=hit)
        }

    @classmethod
    def _build_query_result(cls, hit):
        raise NotImplementedError


class CocktailQueryResult(QueryResult):

    @classmethod
    def _build_query_result(cls, hit):
        return {
            'cocktail_slug': hit.slug,
            'cocktail_display_name': hit.display_name,
            'spec_slug': hit.spec.slug,
            'spec_display_name': hit.spec.display_name,
            'component_display_names': [component['display_name'] for component in hit.spec.components],
        }


class BaseQuery:
    def __init__(self):
        self._param_mappings = {}

    def add_parameter_field_mapping(self, parameter, fields):
        self._param_mappings[parameter] = fields

    def get_parameter_field_mapping(self, parameter):
        fields = self._param_mappings.get(parameter)
        if fields is None:
            raise KeyError("No parameter-field mapping for %s" % parameter)
        logging.info("%s maps to %s" % (parameter, fields))
        return fields


class CocktailQuery(BaseQuery):
    def __init__(self, name=None, components=None, name_or_query='bool', sort='_score'):
        super().__init__()
        self.input_parameters = {
            'name': name,
            'components': components,
        }

        self._build_parameter_field_mappings()

        self.query_parameters = {
            'name_or_query': name_or_query,
            'must': self._build_query_conditions()
        }

        self.sort = sort

    def execute(self):
        results = RecipeIndex.search()[0:1000].query(**self.query_parameters).sort(self.sort).execute()
        return self._generate_results(results=results)

    def _build_query_conditions(self):
        musts = []
        if self.input_parameters['name']:
            musts.append(QueryParameter(query=self.input_parameters['name'], fields=self.get_parameter_field_mapping('name')))
        for component in self.input_parameters['components']:
            if not component or component == '':
                continue
            musts.append(QueryParameter(query=component, fields=self.get_parameter_field_mapping('component')))

        return musts

    def _build_parameter_field_mappings(self):
        self.add_parameter_field_mapping('name', ['spec.display_name', 'spec.slug', 'display_name', 'slug'])
        self.add_parameter_field_mapping('component', ['spec.components.slug', 'spec.components.display_name', 'spec.components.parents'])

    @staticmethod
    def _generate_results(results):
        return [CocktailQueryResult(result) for result in results]
