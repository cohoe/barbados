from barbados.objects.base import BaseObject


class Origin(BaseObject):
    def __init__(self, creator=None, venue=None, location=None, year=None, story=None, era=None):
        self.creator = creator
        self.venue = venue
        self.location = location
        self.year = year
        self.story = story
        self.era = era

    def __repr__(self):
        if hasattr(self, 'location'):
            return "Barbados::Object::Origin[%s]" % self.location
        else:
            return "Barbados::Object::Origin[]"

    def serialize(self, serializer):
        serializer.add_property('creator', self.creator, even_if_empty=False)
        serializer.add_property('venue', self.venue, even_if_empty=False)
        serializer.add_property('location', self.creator, even_if_empty=False)
        serializer.add_property('year', self.year, even_if_empty=False)
        serializer.add_property('story', self.story, even_if_empty=False)
        serializer.add_property('era', self.era, even_if_empty=False)
