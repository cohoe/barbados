import os
import logging


class ValidationException(Exception):
    pass


class FatalException(Exception):
    def __init__(self, exception):
        logging.error("A fatal error has occurred: %s" % exception)
        logging.error("PID %i is shutting down." % os.getpid())
        exit(1)


class ServiceUnavailableException(Exception):
    pass
