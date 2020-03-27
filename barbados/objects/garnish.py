from barbados.objects.slug import Slug
from barbados.objects.displayname import DisplayName


class Garnish:
    """
    @TODO this may someday get more fancy, but for now it's just a more specific version of the Text object.
    Someday the direct name part might be able to go away.
    """
    def __init__(self, name, display_name=None, slug=None):
        self.name = name
        self.slug = slug
        self.display_name = display_name

        if self.slug is None:
            self.slug = Slug(name)
        if self.display_name is None:
            self.display_name = DisplayName(name)

    def __repr__(self):
        return "Barbados::Objects::Garnish[%s]" % self.slug

    def serialize(self, serializer):
        serializer.add_property('slug', self.slug)
        serializer.add_property('display_name', self.display_name)