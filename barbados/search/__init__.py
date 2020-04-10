import logging
from elasticsearch_dsl.query import Bool


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
                'hit': cls._serialize_hit(hit=hit)
            })
        return response

    @classmethod
    def _serialize_hit(cls, hit):
        """
        Required function to build a dictionary of attributes to return from the index.
        :param hit: ElasticSearch result.
        :return: dict of attributes.
        """
        raise NotImplementedError


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
    def result_class(self):
        """
        Define the class that represents results of this search.
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
        logging.info("Got %s results." % results.hits.total.value)
        return self.result_class(hits=results)

    def add_query_parameter(self, parameter, query_class, query_key, **attributes):
        """
        Define a queriable parameter for this search index.
        :param parameter: URL/input parameter to key from.
        :param query_class: ElasticSearch DSL query class.
        :param query_key: ElasticSearch query key field (usually not the same as an input parameter)
        :param attributes: Dictionary of extra params to pass to the query_class consturctor
        :return: None
        """
        self.query_parameters[parameter] = {
            'parameter': parameter,
            'query_class': query_class,
            'query_key': query_key,
            'attributes': attributes
        }

    def get_query_condition(self, parameter, value):
        """
        Build an ElasticSearch query object by looking up the parameter settings
        and assigning an input value for the condition.
        :param parameter: URL query parameter.
        :param value: The value to look for in the index.
        :return: Query() child object.
        """
        settings = self.query_parameters.get(parameter)
        if not settings:
            raise KeyError("Parameter %s has no query parameters defined." % parameter)

        query_class_parameters = {**{settings.get('query_key'): value}, **settings.get('attributes')}
        return settings.get('query_class')(**query_class_parameters)

    def _build_search_query(self):
        """
        Construct the ElasticSearch query object containing all conditions
        :return:
        """
        musts = []
        for parameter in self.supported_parameters:
            values = getattr(self, parameter, None)
            if not values:
                continue

            # We split in the URL based on ,'s.
            values = values.split(',')

            for value in values:
                if not value:
                    continue
                musts.append(self.get_query_condition(parameter=parameter, value=value))

        logging.info("Search Conditions are %s" % musts)
        return Bool(must=musts)
