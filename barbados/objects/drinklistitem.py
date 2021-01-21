from barbados.objects.base import BaseObject


class DrinkListItem(BaseObject):
    """
    A DrinkListitem is a glorified hint/pointer to a specific item
    in a DrinkList. Right now this is only coded for either a "cocktail"
    or a specific Spec of a particular Cocktail.
    @TODO add a Kind field and make this generic?
    @TODO deal with notes
    """

    def __init__(self, cocktail_slug, spec_slug=None, notes=None, highlight=False):
        if notes is None:
            notes = []
        self.notes = notes
        self.cocktail_slug = cocktail_slug
        self.spec_slug = spec_slug
        self.highlight = highlight

    def __repr__(self):
        return "Barbados::Objects::DrinkListItem[%s]" % self.cocktail_slug

    def serialize(self, serializer):
        serializer.add_property('cocktail_slug', self.cocktail_slug)
        serializer.add_property('spec_slug', self.spec_slug)
        serializer.add_property('highlight', self.highlight)
