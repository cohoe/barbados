class BaseOccurrence:
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html
    pass


class MustOccurrence(BaseOccurrence):
    occur = 'must'


class FilterOccurrence(BaseOccurrence):
    occur = 'filter'


class ShouldOccurrence(BaseOccurrence):
    occur = 'should'


class MustNotOccurrence(BaseOccurrence):
    occur = 'must_not'


class OccurrenceFactory:
    """
    Factory to manage the existence of the various supported
    ElasticSearch Boolean Occurrence classes.
    """
    def __init__(self):
        self._occurrences = {}

    def register(self, occurrence):
        """
        Register an occurrence class with the factory.
        :param occurrence: Child class of BaseOccurrence.
        :return: None
        """
        self._occurrences[occurrence.occur] = occurrence

    def get_occurrence(self, occurrence):
        """
        Retrieve a particular occurrence class based on its key.
        :param occurrence: String key identifier of the occurrence.
        :return: Child class of BaseOccurrence.
        """
        occurrence_class = self._occurrences.get(occurrence)
        if not occurrence_class:
            raise ValueError(occurrence)
        return occurrence_class


Occurrences = OccurrenceFactory()
Occurrences.register(MustOccurrence)
Occurrences.register(FilterOccurrence)
Occurrences.register(ShouldOccurrence)
Occurrences.register(MustNotOccurrence)
