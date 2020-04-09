import logging


class QueryParameter:
    """
    This class defines an ElasticSearch query parameter. Designed for multi_match.
    https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-queries.html
    This is not really an object, more of a class manifestation of a dict.
    """
    # def __new__(cls, query, fields, kind='multi_match', type_='phrase_prefix'):
    def __new__(cls, kind, **kwargs):
        if kind is 'multi_match':
            return {
                kind: {
                    'query': kwargs.get('query'),
                    'type': 'phrase_prefix',
                    'fields': kwargs.get('fields'),
                }
            }
        elif kind is 'prefix':
            return {
                kind: {
                    kwargs.get('fields')[0]: { # @TODO dont reuse
                        'value': kwargs.get('query') # @TODO dont reuse
                    }
                }
            }
        else:
            raise Exception("Unsupported QueryParameter kind: %s" % kind)


class BaseQuery:
    """
    Generic class to manage querying an ElasticSearch index. This class is wicked yuuuge
    so that the specific index implementations don't have to be.
    """
    def __init__(self, index_class, result_class, sort, input_parameters):
        self.index_class = index_class
        self.result_class = result_class
        self._param_mappings = {}
        self.input_parameters = input_parameters
        self.query_parameters = {}
        self.query_config = {}
        self.sort = sort

    def add_parameter_field_mapping(self, parameter, fields):
        """
        Query parameters (input via API) map to a set of fields in the index.
        These are referred to as "parameter-field mappings". This method adds
        a new mapping.
        :param parameter: Query parameter.
        :param fields: list of fields to search when querying on this parameter.
        :return: None
        """
        self._param_mappings[parameter] = fields

    def get_parameter_field_mapping(self, parameter):
        """
        Look up the fields to search for a particular parameter.
        :param parameter: Query parameter.
        :return: List of fields (strings), or KeyError
        """
        fields = self._param_mappings.get(parameter)
        if fields is None:
            raise KeyError("No parameter-field mapping for %s" % parameter)
        logging.info("%s maps to %s" % (parameter, fields))
        return fields

    def add_query_parameter(self, parameter, type_):
        """
        Define an input parameter of this query. To determine appropriate search
        settings its type is also needed.
        :param parameter: Query parameter.
        :param type_: Python type class corresponding to the expected value of the parameter.
        :return: None
        """
        self.query_parameters[parameter] = type_

    @staticmethod
    def _generate_results(results, result_class):
        """
        Generate a list of QueryResult-ish objects to return to the caller
        :param results: List of ElasticSearch results.
        :param result_class: QueryResult-ish class to turn everything into.
        :return: List of result_class objects.
        """
        return [result_class(result) for result in results]

    def _build_parameter_field_mappings(self):
        """
        Define all parameter-field mappings for a particular BaseQuery-ish object.
        :return: None
        """
        raise NotImplementedError

    def _build_query_parameters(self):
        """
        Define all query input parameters for this BaseQuery-ish object.
        :return: None
        """
        raise NotImplementedError

    def _build_query_condition(self, parameter, value, kind='prefix'):
        """
        Build an ElasticSearch query condition based on a parameters value and its fields.
        :param parameter: The query parameter to then go find its fields (look for parameter-field mapping).
        :param value: The value to look for in the index.
        :return: QueryParameter or None
        """
        if not value:
            return

        return QueryParameter(kind=kind, query=value, fields=self.get_parameter_field_mapping(parameter))

    def _build_query_conditions(self):
        """
        Build a list of all query conditions.
        :return: List of QueryParameter
        """
        conditions = []
        for parameter, type_ in self.query_parameters.items():
            logging.info("Building condition for %s of type %s" % (parameter, type_))
            if type_ is str:
                conditions.append(self._build_query_condition(parameter=parameter, value=self.input_parameters.get(parameter)))
            elif type_ is list:
                for param in self.input_parameters.get(parameter):
                    conditions.append(self._build_query_condition(parameter=parameter, value=param))

        # https://www.geeksforgeeks.org/python-remove-none-values-from-list/
        return list(filter(None, conditions))

    def execute(self):
        """
        Actually talk to ElasticSearch and run the query.
        :return: List of QueryResult-ish objects.
        """
        results = self.index_class.search()[0:1000].query(**self.query_config).sort(self.sort).execute()
        return self._generate_results(results=results, result_class=self.result_class)
