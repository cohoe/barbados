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
    def __init__(self, slug, status, substitutes=None):
        if substitutes is None:
            substitutes = []
        self.slug = slug
        # @TODO enforcement without isinstance() since its not an instance.
        self.status = status
        self.substitutes = substitutes

    def __repr__(self):
        return "Barbados::Resolution[%s]" % self.slug

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('status', self.status.status)
        serializer.add_property('substitutes', self.substitutes)
