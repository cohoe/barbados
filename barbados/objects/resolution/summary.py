from barbados.objects.resolution import Resolution
from barbados.serializers import ObjectSerializer
from barbados.objects.resolution.results import ResolutionResults
from barbados.objects.base import BaseObject


class RecipeResolutionSummary(BaseObject):
    """
    Summary of a comparison between an Inventory and a Spec. Figure out
    what this inventory has, both explicitly and implicitly.
    """
    def __init__(self, inventory_id, cocktail_slug, spec_slug, components, alpha, construction_slug,
                 garnish, component_count=0, status_count=0, citations=None):
        # @TODO this seems sketchy....
        if citations is None:
            citations = []
        self.inventory_id = inventory_id
        self.cocktail_slug = cocktail_slug
        self.spec_slug = spec_slug
        self.components = components
        self.component_count = component_count
        self.alpha = alpha
        self.construction_slug = construction_slug
        self.citations = citations
        self.garnish = garnish

    def __repr__(self):
        return "Barbados::Objects::Resolution::RecipeResolutionSummary[%s]" % self.index_id

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
        counts = {key: 0 for key in ResolutionResults.get_resolution_statuses()}
        for r in self.components:
            status_key = r.status.status
            try:
                counts.update({status_key: counts[status_key]+1})
            except KeyError:
                counts.update({status_key: 1})
        return counts

    @property
    def index_id(self):
        """
        The document ID for the index. Has to be unique.
        :return:
        """
        return "%s::%s::%s" % (self.inventory_id, self.cocktail_slug, self.spec_slug)

    def serialize(self, serializer):
        serializer.add_property('inventory_id', self.inventory_id)
        serializer.add_property('cocktail_slug', self.cocktail_slug)
        serializer.add_property('spec_slug', self.spec_slug)
        serializer.add_property('components', [ObjectSerializer.serialize(res, serializer.format) for res in self.components])
        serializer.add_property('status_count', self.status_count)
        serializer.add_property('component_count', self.component_count)
        serializer.add_property('alpha', self.alpha)
        serializer.add_property('construction_slug', self.construction_slug)
        serializer.add_property('citations', [ObjectSerializer.serialize(citation, serializer.format) for citation in self.citations])
        serializer.add_property('garnish', [ObjectSerializer.serialize(garnish, serializer.format) for garnish in self.garnish])
