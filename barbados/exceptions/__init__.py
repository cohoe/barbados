import os
import logging
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


class FactoryUpdateException(Exception):
    """
    The factory tried to update something but it couldn't. Probably because
    you're trying to be naughty and change the ID or something like that.
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
