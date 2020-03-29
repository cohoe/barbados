from barbados.objects.displayname import DisplayName


class Construction:
    def __init__(self, slug, display_name=None):
        self.slug = slug
        self.display_name = display_name

        if self.display_name is None:
            self.display_name = DisplayName(slug)

    def __repr__(self):
        return "Barbados::Objects::Construction[%s]" % self.slug

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('display_name', self.display_name)
