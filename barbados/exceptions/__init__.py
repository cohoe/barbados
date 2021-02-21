import os
import logging
# @TODO wrap this into the search service
from elasticsearch.exceptions import NotFoundError


class ValidationException(Exception):
    """
    Used for validators.
    Probably 400?
    """
    pass


class FactoryException(Exception):
    """
    Used for factories when they can't do something.
    Probably 500?
    """
    pass


class SearchException(Exception):
    """
    Used for search.
    Probably 400?
    """
    pass


class FatalException(Exception):
    def __init__(self, exception):
        logging.error("A fatal error has occurred: %s" % exception)
        logging.error("PID %i is shutting down." % os.getpid())
        exit(1)


class ServiceUnavailableException(Exception):
    pass
