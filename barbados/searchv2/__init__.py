import logging
from elasticsearch_dsl.query import MultiMatch, Prefix, Bool
from barbados.indexes import RecipeIndex


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


class BaseSearch:
    def __init__(self):
        self.q = None
        self.sort = None
        self.query_parameters = {}

        self._build_query_parameters()

    @property
    def index_class(self):
        raise NotImplementedError

    @property
    def result_class(self):
        raise NotImplementedError

    def _build_query_parameters(self):
        raise NotImplementedError

    def execute(self):
        """
        Actually talk to ElasticSearch and run the query.
        :return: SearchResults child class.
        """
        results = self.index_class.search()[0:1000].query(self.q).sort(self.sort).execute()
        logging.info("Got %s results." % results.hits.total.value)
        return self.result_class(hits=results)

    def add_query_parameter(self, parameter, query_class, query_key, **attributes):
        self.query_parameters[parameter] = {
            'parameter': parameter,
            'query_class': query_class,
            'query_key': query_key,
            'attributes': attributes
        }
        logging.info("%s: %s" % (parameter, self.query_parameters[parameter]))

    def get_query_object(self, parameter, value):
        settings = self.query_parameters.get(parameter)
        if not settings:
            raise KeyError("Parameter %s has no query parameters defined." % parameter)

        query_class_parameters = {**{settings.get('query_key'): value}, **settings.get('attributes')}
        return settings.get('query_class')(**query_class_parameters)


class CocktailSearch(BaseSearch):
    index_class = RecipeIndex
    result_class = CocktailSearchResults

    def __init__(self, name, components, alpha, sort='_score'):
        super().__init__()
        logging.info("Searching on name=%s,components=%s,alpha=%s" % (name, components, alpha))
        names = name.split(',')
        components = components.split(',')
        alphas = alpha.split(',')

        musts = []

        for component in components:
            # @TODO fix this
            if not component:
                continue
            musts.append(self.get_query_object(parameter='components', value=component))

        for name in names:
            if not name:
                continue
            musts.append(self.get_query_object(parameter='name', value=name))

        # Need to do ||, not &&
        for alpha in alphas:
            if not alpha:
                continue
            musts.append(self.get_query_object(parameter='alpha', value=alpha))

        print(musts)
        self.q = Bool(must=musts)
        self.sort = sort

    def _build_query_parameters(self):
        self.add_query_parameter(parameter='components', query_class=MultiMatch, query_key='query', type='phrase_prefix',
                                 fields=['spec.components.slug', 'specs.component.display_name', 'spec.components.parents'])
        self.add_query_parameter(parameter='name', query_class=MultiMatch, query_key='query', type='phrase_prefix',
                                 fields=['spec.name', 'display_name'])
        self.add_query_parameter(parameter='alpha', query_class=Prefix, query_key='alpha')
