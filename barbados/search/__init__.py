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
    def __init__(self, index_class, result_class, sort, input_parameters):
        self.index_class = index_class
        self.result_class = result_class
        self._param_mappings = {}
        self.input_parameters = input_parameters
        self.query_parameters = {}
        self.query_config = {}
        self.sort = sort

    def add_parameter_field_mapping(self, parameter, fields):
        self._param_mappings[parameter] = fields

    def get_parameter_field_mapping(self, parameter):
        fields = self._param_mappings.get(parameter)
        if fields is None:
            raise KeyError("No parameter-field mapping for %s" % parameter)
        logging.info("%s maps to %s" % (parameter, fields))
        return fields

    def add_query_parameter(self, parameter, type_):
        self.query_parameters[parameter] = type_

    @staticmethod
    def _generate_results(results, result_class):
        return [result_class(result) for result in results]

    def _build_parameter_field_mappings(self):
        raise NotImplementedError

    def _build_query_parameters(self):
        raise NotImplementedError

    def _build_query_condition(self, parameter, value):
        if not value:
            return

        return QueryParameter(query=value, fields=self.get_parameter_field_mapping(parameter))

    def _build_query_conditions(self):
        conditions = []
        for parameter, type_ in self.query_parameters.items():
            logging.info("Building condition for %s of type %s" % (parameter, type_))
            if type_ is str:
                logging.info("%s is a STRING!" % parameter)
                conditions.append(self._build_query_condition(parameter=parameter, value=self.input_parameters.get(parameter)))
            elif type_ is list:
                logging.info("%s is a LIST!" % parameter)
                for param in self.input_parameters.get(parameter):
                    conditions.append(self._build_query_condition(parameter=parameter, value=param))

        # https://www.geeksforgeeks.org/python-remove-none-values-from-list/
        return list(filter(None, conditions))

    def execute(self):
        results = self.index_class.search()[0:1000].query(**self.query_config).sort(self.sort).execute()
        return self._generate_results(results=results, result_class=CocktailQueryResult)


class CocktailQuery(BaseQuery):
    def __init__(self, input_parameters, index_class=RecipeIndex, result_class=CocktailQueryResult, name_or_query='bool', sort='_score'):
        super().__init__(index_class, result_class, sort, input_parameters)

        self._build_parameter_field_mappings()
        self._build_query_parameters()

        self.query_config = {
            'name_or_query': name_or_query,
            'must': self._build_query_conditions()
        }

    def _build_parameter_field_mappings(self):
        self.add_parameter_field_mapping('name', ['spec.display_name', 'spec.slug', 'display_name', 'slug'])
        self.add_parameter_field_mapping('components', ['spec.components.slug', 'spec.components.display_name', 'spec.components.parents'])

    def _build_query_parameters(self):
        self.add_query_parameter('name', str)
        self.add_query_parameter('components', list)
