from barbados.objects.resolution.status import ResolutionStatuses


class SpecComponentResolution:
    """
    A SpecComponentResolution represents a comparison of an ingredient (SpecComponent) to what you have in your Inventory. Generally this
    can mean you have it (Direct), you can substitute for it (Implicit), or it's Missing entirely. This calculation is performed using
    the IngredientTree.
    """
    def __init__(self, slug, status, substitutes=None, parent=None, parents=None):
        if parents is None:
            parents = []
        if substitutes is None:
            substitutes = []
        self.slug = slug
        self.status = ResolutionStatuses.get_status(status)
        self.substitutes = substitutes
        self.parent = parent
        self.parents = parents

    def __repr__(self):
        return "Barbados::Objects::SpecComponentResolution[%s]" % self.slug

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('status', self.status.status)
        serializer.add_property('substitutes', self.substitutes)
        serializer.add_property('parent', self.parent)
        serializer.add_property('parents', self.parents)
