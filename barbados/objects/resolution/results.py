class BaseResolutionResult:
    """
    ResolutionResults define the responses to whether you have something
    in your inventory. THis defines a common base class to inherit from.
    Heads up that __repr__() doesn't show up in child classes so even if
    I were to define it here it would not be useful.
    """
    @property
    def status(self):
        raise NotImplementedError()


class DirectResolutionResult(BaseResolutionResult):
    status = 'DIRECT'


class ImplicitResolutionResult(BaseResolutionResult):
    status = 'IMPLICIT'


class MissingResolutionResult(BaseResolutionResult):
    status = 'MISSING'


class ResolutionResultsFactory:
    """
    Handler for managing the various ResolutionResults.
    """
    def __init__(self):
        self._resolutions = {}

    def register(self, resolution):
        """
        Register a ResolutionResult for usage.
        :param resolution: ResolutionResult class.
        :return: None
        """
        self._resolutions[resolution.status] = resolution

    def get_resolution(self, key):
        """
        Find the BaseResolution child class based on its key. Sometimes we
        might be given a class already so we do a sniff test and simply
        return it if that happens.
        :param key: Status key (string or BaseResolution child).
        :return: BaseResolution child class.
        """
        try:
            status_value = key.status
            return key
        except AttributeError:
            pass
        r = self._resolutions.get(key)
        if not r:
            raise KeyError("No resolution found for '%s'." % key)

        return r

    def get_resolution_statuses(self):
        """
        Get a list of all status strings for the various ResolutionResult
        classes that are registered.
        :return: List of Strings.
        """
        return list(self._resolutions.keys())


ResolutionResults = ResolutionResultsFactory()
ResolutionResults.register(DirectResolutionResult)
ResolutionResults.register(ImplicitResolutionResult)
ResolutionResults.register(MissingResolutionResult)