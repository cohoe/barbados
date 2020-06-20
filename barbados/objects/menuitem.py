class MenuItem:
    """
    A MenuItem is a glorified hint/pointer to a specific item
    in a menu. Right now this is only coded for either a "cocktail"
    or a specific Spec of a particular Cocktail.
    @TODO add a Kind field and make this generic?
    """

    def __init__(self, cocktail_slug, spec_slug=None):
        self.cocktail_slug = cocktail_slug
        self.spec_slug = spec_slug

    def __repr__(self):
        return "Barbados::Objects::MenuItem[%s]" % self.cocktail_slug

    def serialize(self, serializer):
        serializer.add_property('cocktail_slug', self.cocktail_slug)
        serializer.add_property('spec_slug', self.spec_slug)
