from barbados.objects.displayname import DisplayName


class Glassware:
    def __init__(self, slug, display_name=None):
        self.slug = slug

        if display_name is None:
            display_name = DisplayName(slug)

        self.display_name = display_name

    def __repr__(self):
        return "Barbados::Objects:Glassware[%s]" % self.slug

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('display_name', self.display_name)
