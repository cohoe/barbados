from barbados.search import SearchBase
from elasticsearch_dsl.query import MatchPhrase, Wildcard, Prefix, Match
from barbados.indexes.inventoryspecresolution import InventorySpecResolution
from barbados.search.occurrences import ShouldOccurrence


class InventorySpecResolutionSearch(SearchBase):
    index_class = InventorySpecResolution

    def _build_query_parameters(self):
        self.add_query_parameter(url_parameter='components',
                                 url_parameter_type=list,
                                 query_class=MatchPhrase,
                                 fields=['components.slug', 'components.parent'])
        self.add_query_parameter(url_parameter='missing',
                                 query_class=Match,
                                 url_parameter_type=range,
                                 # occurrence=ShouldOccurrence,
                                 fields=['status_count.MISSING'])
        # self.add_query_parameter(url_parameter='alpha',
        #                          query_class=Prefix,
        #                          fields=['alpha'])
        # self.add_query_parameter(url_parameter='construction',
        #                          query_class=Match,
        #                          fields=['spec.construction.slug'])
        # self.add_query_parameter(url_parameter='component_count',
        #                          query_class=Match,
        #                          fields=['spec.component_count'])
        # self.add_query_parameter(url_parameter='no_components',
        #                          url_parameter_type=list,
        #                          query_class=MatchPhrase,
        #                          invert=True,
        #                          fields=['spec.components.slug', 'spec.component.display_name', 'spec.components.parents'])
#