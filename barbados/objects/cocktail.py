from .status import Status


class Cocktail:
    def __init__(self, display_name, status, origin, specs, citations, notes, tags, slug):
        self.display_name = display_name
        self.status = status
        self.origin = origin
        self.specs = specs
        self.citations = citations
        self.notes = notes
        self.tags = tags
        self.slug = slug

        if not isinstance(self.status, Status):
            print("Status is not of type Status")

    @property
    def spec_count(self):
        return len(self.specs)

    def __repr__(self):
        return "<Barbados::Object::Cocktail[slug=%s]>" % self.slug

    def serialize(self):
        """
        Return a JSON-encodable dictionary representing all aspects of this
        object, generally used for search.
        :return:
        """
        ser = {
            'display_name': self.display_name,
            'slug': self.slug,
            'status': self.status.color,
            'origin': self.origin.serialize(),
            'specs': [spec.serialize() for spec in self.specs],
            'spec_count': self.spec_count,
            'citations': [citation.serialize() for citation in self.citations],
            'notes': [note.serialize() for note in self.notes],
        }
        return ser
