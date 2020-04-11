from barbados.text import DisplayName


class Garnish:
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
        serializer.add_property('note', self.note, even_if_empty=False)
        serializer.add_property('quantity', self.quantity, even_if_empty=False)
