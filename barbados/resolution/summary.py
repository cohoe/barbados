from barbados.resolution import Resolution
from barbados.serializers import ObjectSerializer


class SpecResolutionSummary:
    """
    Summary of a comparison between an Inventory and a Spec. Figure out
    what this inventory has, both explicitly and implicitly.
    """
    def __init__(self, cocktail_slug, spec_slug='ALL'):
        self.cocktail_slug = cocktail_slug
        self.spec_slug = spec_slug
        self.components = []

    def __repr__(self):
        return "Barbados::Resolution::SpecResolutionSummary[%s::%s]" % (self.cocktail_slug, self.spec_slug)

    def add_component(self, resolution):
        """
        Add a component resolution to this summary.
        :param resolution: barbados.resolution.Resolution child.
        :return: None
        """
        # Test the incoming
        if not isinstance(resolution, Resolution):
            raise ValueError("Bad resolution type. %s" % Resolution)

        # Add the resolution to the list of components for this spec.
        self.components.append(resolution)

    @property
    def status_count(self):
        """
        Generate a summary of the count of each kind of status for this
        resolution. Example: {3x direct, 1x implicit, 1x missing}.
        :return: Dict
        """
        counts = {}
        for r in self.components:
            status_key = r.status.status
            try:
                counts.update({status_key: counts[status_key]+1})
            except KeyError:
                counts.update({status_key: 1})
        return counts

    def serialize(self, serializer):
        serializer.add_property('cocktail_slug', self.cocktail_slug)
        serializer.add_property('spec_slug', self.spec_slug)
        serializer.add_property('components', [ObjectSerializer.serialize(res, serializer.format) for res in self.components])
        serializer.add_property('status_count', self.status_count)
