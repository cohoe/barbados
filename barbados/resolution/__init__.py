from barbados.serializers import ObjectSerializer


class BaseResolution:
    @property
    def status(self):
        raise NotImplementedError()


class DirectResolution(BaseResolution):
    status = 'DIRECT'


class ImplicitResolution(BaseResolution):
    status = 'IMPLICIT'


class MissingResolution(BaseResolution):
    status = 'MISSING'


class Resolution:
    def __init__(self, slug, status, substitutes=[]):
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


class SpecResolutionSummary:
    def __init__(self, cocktail_slug, spec_slug='ALL'):
        self.cocktail_slug = cocktail_slug
        self.spec_slug = spec_slug
        self.components = []

    def __repr__(self):
        return "Barbados::SpecResolutionSummary[%s::%s]" % (self.cocktail_slug, self.spec_slug)

    def add_component(self, resolution):
        if not isinstance(resolution, Resolution):
            raise ValueError("Bad resolution type. %s" % Resolution)
        self.components.append(resolution)

    def serialize(self, serializer):
        serializer.add_property('cocktail_slug', self.cocktail_slug)
        serializer.add_property('spec_slug', self.spec_slug)
        serializer.add_property('components', [ObjectSerializer.serialize(res, serializer.format) for res in self.components])
