from elasticsearch_dsl.query import MatchAll


class BaseIndex:
    """
    Base class for the ElasticSearch Index metadata class contained
    within each Index.
    """
    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0,
    }


class BarbadosIndex:
    """
    Base class for our interactions with ElasticSearch indexes.
    """

    @classmethod
    def scan(cls):
        """
        Return a list of all documents within this index.
        :return: Generator that will yield every document (as a list... kinda)
        """
        scan_request = cls._index.search().query(MatchAll())
        response = scan_request.scan()
        return response

    @classmethod
    def delete_all(cls):
        """
        Delete all documents within this index.
        :return: Count of the documents that were deleted.
        """
        hits = cls.scan()

        # We track this independently of a len() thing because the
        # list dynamically changes.
        counter = 0

        # Iterate through the hits and delete them.
        for hit in hits:
            hit.delete()
            counter += 1

        # Return the count of documents we shredded.
        # Gotta hide the evidence.
        return counter
