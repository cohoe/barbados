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


class BaseQuery:
    def __init__(self):
        self.q = None
        self.sort = None

    @property
    def index_class(self):
        raise NotImplementedError

    @property
    def result_class(self):
        raise NotImplementedError

    def execute(self):
        """
        Actually talk to ElasticSearch and run the query.
        :return: SearchResults child class.
        """
        results = self.index_class.search()[0:1000].query(self.q).sort(self.sort).execute()
        logging.info("Got %s results." % results.hits.total.value)
        return self.result_class(hits=results)


class CocktailQuery(BaseQuery):

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
            musts.append(MultiMatch(query=component, type='phrase_prefix',
                                    fields=['spec.components.slug', 'specs.component.display_name', 'spec.components.parents']))

        for name in names:
            if not name:
                continue
            musts.append(MultiMatch(query=name, type='phrase_prefix', fields=['spec.name', 'display_name']))

        # Need to do ||, not &&
        for alpha in alphas:
            if not alpha:
                continue
            musts.append(Prefix(alpha=alpha))

        print(musts)
        self.q = Bool(must=musts)
        self.sort = sort