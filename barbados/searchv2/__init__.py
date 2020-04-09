import logging
from elasticsearch_dsl.query import MultiMatch, Prefix
from barbados.indexes import RecipeIndex


class CocktailQuery:
    # def _build_field_queries(self):
    #     self.add_field_query(parameter='name', parameter_type=list, kind=MultiMatch,
    #                          fields=['spec.display_name', 'spec.slug', 'display_name', 'slug'])
    def __new__(cls, name, components):
        logging.info("Searching on name=%s,components=%s" % (name, components))
        musts = []
        for component in components:
            # @TODO fix this
            if component == '':
                continue
            musts.append({
                'multi_match': {
                    'query': component,
                    'type': 'phrase_prefix',
                    'fields': ['spec.components.slug', 'specs.component.display_name', 'spec.components.parents'],
                }
            })

        if name:
            musts.append({
                'multi_match': {
                    'query': name,
                    'type': 'phrase_prefix',
                    'fields': ['spec.name', 'display_name'],
                }
            })

        print(musts)

        query_params = {
            'name_or_query': 'bool',
            'must': musts
        }

        results = RecipeIndex.search()[0:1000].query(**query_params).sort('_score').execute()
        logging.info("Got %s results." % results.hits.total.value)

        slugs = []
        for hit in results:
            logging.info("%s :: %s" % (hit.slug, hit.meta.score))
            slugs.append({'slug': hit.slug, 'score': hit.meta.score})

        return slugs
