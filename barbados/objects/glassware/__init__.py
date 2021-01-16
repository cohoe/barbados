from barbados.objects.text import DisplayName


class Glassware:
    def __init__(self, slug, display_name=None):
        if not display_name:
            display_name = DisplayName(slug)

        self.slug = slug
        self.display_name = display_name

    def __repr__(self):
        return "Barbados::Objects:Glassware[%s]" % self.slug

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('display_name', self.display_name)
