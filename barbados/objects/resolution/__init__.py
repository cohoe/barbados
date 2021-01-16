class BaseResolution:
    @property
    def status(self):
        raise NotImplementedError()

    # @TODO this doesn't work. But we might not care.
    def __repr__(self):
        return "Barbados::Resolution::%s[]" % self.__class__.__name__


class DirectResolution(BaseResolution):
    status = 'DIRECT'


class ImplicitResolution(BaseResolution):
    status = 'IMPLICIT'


class MissingResolution(BaseResolution):
    status = 'MISSING'


class Resolution:
    def __init__(self, slug, status, substitutes=None, parent=None, parents=None):
        if parents is None:
            parents = []
        if substitutes is None:
            substitutes = []
        self.slug = slug
        # @TODO enforcement without isinstance() since its not an instance.
        self.status = status
        self.substitutes = substitutes
        self.parent = parent
        self.parents = parents

    def __repr__(self):
        return "Barbados::Resolution[%s]" % self.slug

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('status', self.status.status)
        serializer.add_property('substitutes', self.substitutes)
        serializer.add_property('parent', self.parent)
        serializer.add_property('parents', self.parents)


class ResolutionFactory:
    def __init__(self):
        self._resolutions = {}

    def register_resolution(self, resolution):
        self._resolutions[resolution.status] = resolution

    def get_resolution(self, key):
        r = self._resolutions.get(key)
        if not r:
            raise KeyError("No resolution found for '%s'." % key)

        return r

    def get_resolution_statuses(self):
        return list(self._resolutions.keys())


resolution_factory = ResolutionFactory()
resolution_factory.register_resolution(DirectResolution)
resolution_factory.register_resolution(ImplicitResolution)
resolution_factory.register_resolution(MissingResolution)
