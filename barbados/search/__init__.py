from barbados.services.logging import Log
from elasticsearch_dsl.query import Bool, Wildcard, MatchPhrase, Prefix, Match
from barbados.exceptions import ValidationException



class SearchResults:
    """
    Standardized search response object. Provides the ElasticSearch document ID and
    the score, along with the actual result as defined by the appropriate
    SearchResult child class. This is not really an object, more of a class manifestation
    of a dict.
    """

    def __new__(cls, hits):
        response = []
        for hit in hits:
            response.append({
                'id': hit.meta.id,
                'score': hit.meta.score,
                'hit': hit.to_dict()
            })
        return response


class SearchBase:
    """
    Generic class to manage querying an ElasticSearch index. This class is wicked yuuuge
    so that the specific index implementations don't have to be.
    """

    def __init__(self, **kwargs):
        self.query_parameters = {}
        self._build_query_parameters()

        for key, value in kwargs.items():
            if key not in self.supported_parameters:
                raise KeyError("Query parameter %s is not supported" % key)
            setattr(self, key, value)

        self.q = self._build_search_query()

    @property
    def index_class(self):
        """
        Define the class of the ElasticSearch index for this search.
        :return:
        """
        raise NotImplementedError

    @property
    def supported_parameters(self):
        """
        Return a list of the supported query parameters of the class.
        :return: List of Strings.
        """
        return list(self.query_parameters.keys())

    def _build_query_parameters(self):
        """
        Perform a series of self.add_query_parameter() to define what the parameters
        are that this class supports.
        :return:
        """
        raise NotImplementedError

    def execute(self, sort='_score'):
        """
        Actually talk to ElasticSearch and run the query.
        :param sort: ElasticSearch attribute on which to sort the results.
        :return: SearchResults child class.
        """
        results = self.index_class.search()[0:1000].query(self.q).sort(sort).execute()
        Log.info("Got %s results." % results.hits.total.value)
        return SearchResults(hits=results)

    def add_query_parameter(self, url_parameter, query_class, fields, url_parameter_type=str, invert=False, **attributes):
        """
        Define a queriable parameter for this search index.
        :param url_parameter: URL/input parameter to key from.
        :param url_parameter_type: Python type class of this parameter from the URL.
        :param query_class: ElasticSearch DSL query class.
        :param invert: Turn this from Must to MustNot
        :param attributes: Dictionary of extra params to pass to the query_class consturctor
        :return: None
        """
        self.query_parameters[url_parameter] = {
            'url_parameter': url_parameter,
            'url_parameter_type': url_parameter_type,
            'query_class': query_class,
            'attributes': attributes,
            'invert': invert,
            'fields': fields
        }

    def get_query_condition(self, url_parameter, field, value):
        """
        """
        settings = self.query_parameters.get(url_parameter)
        if not settings:
            raise KeyError("Parameter %s has no query parameters defined." % url_parameter)

        # The resultant query_class_parameters dictionary looks something like:
        # {
        #   'query_key': 'value',
        #   'fields': ['foo', 'bar', 'baz'],
        # }
        # Attributes is the leftover **kwargs from the original function call.
        #query_class_parameters = {**{settings.get('query_key'): value}, **settings.get('attributes')}

        if settings.get('query_class') is Wildcard:
            search_value = "*%s*" % value
            return Wildcard(**{field: {'value': search_value}})
        elif settings.get('query_class') is MatchPhrase:
            return MatchPhrase(**{field: value})
        elif settings.get('query_class') is Prefix:
            return Prefix(**{field: value})
        elif settings.get('query_class') is Match:
            return Match(**{field: {'query': value}})
        else:
            raise KeyError("Unsupported query class")

    def _build_search_query(self):
        """
        "filter" = "must" without scoring. Better for caching.
        
        This function is built for Bool() queries only.
        """
        musts = []
        must_nots = []

        for url_parameter in self.supported_parameters:

            shoulds = []

            raw_value = getattr(self, url_parameter, None)
            if not raw_value:
                continue
            
            expected_value_type = self.query_parameters.get(url_parameter).get('url_parameter_type')
            self._validate_query_parameter(parameter=url_parameter, value=raw_value, type_=expected_value_type)

            fields = self.query_parameters.get(url_parameter).get('fields')

            if expected_value_type is list:
                for value in raw_value:
                    for field in fields:
                        shoulds.append(self.get_query_condition(url_parameter=url_parameter, field=field, value=value))
            elif expected_value_type is str:
                for field in fields:
                    shoulds.append(self.get_query_condition(url_parameter=url_parameter, field=field, value=raw_value))
            else:
                pass

            if self.query_parameters.get(url_parameter).get('invert'):
                must_nots.append(Bool(should=shoulds))
            else:
                musts.append(Bool(should=shoulds))

        Log.info("Search Conditions are MUST=%s MUST_NOT=%s" % (musts, must_nots))
        return Bool(must=musts, must_not=must_nots)

    @staticmethod
    def _validate_query_parameter(parameter, value, type_):
        """
        Ensure that the value of a query parameter matches the expected type.
        This is somewhat redundant now that proper request parsing works on
        the API end, but hey better to be sure right?
        :param parameter: URL parameter.
        :param value: Value as passed by the user (after modeling).
        :param type_: expected python type class.
        :return: None
        """
        if type(value) is not type_:
            raise ValidationException("Value of parameter '%s' is not a '%s' (got '%s')" % (parameter, type_, value))
