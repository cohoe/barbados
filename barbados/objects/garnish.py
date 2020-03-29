from barbados.objects.displayname import DisplayName


class Garnish:
    """
    @TODO this may someday get more fancy, but for now it's just a more specific version of the Text object.
    Someday the direct name part might be able to go away.
    """

    def __init__(self, slug, display_name=None, quantity=None, note=None):
        self.slug = slug
        self.display_name = display_name
        self.note = note
        self.quantity = quantity

        if self.display_name is None:
            self.display_name = DisplayName(slug)

    def __repr__(self):
        return "Barbados::Objects::Garnish[%s]" % self.slug

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('display_name', self.display_name)
        serializer.add_property('note', self.note)
        serializer.add_property('quantity', self.quantity)
