# @TODO Oh gods.... all of this.
from barbados.objects.base import BaseObject
from barbados.serializers import ObjectSerializer


class Citation(BaseObject):
    def __init__(self, title=None, author=None, date=None, publisher=None, page=None, notes=None, href=None, location=None, issue=None):
        self.title = title
        self.author = author
        self.date = date
        self.publisher = publisher
        self.page = page
        self.notes = notes
        self.href = href
        self.location = location
        self.issue = issue

    def to_mla_ish(self, html=False):
        if hasattr(self, 'author'):
            if isinstance(self.author, list):
                author = ', '.join(self.author)
            else:
                author = self.author
        else:
            author = 'Unknown Author'
        author += '. '

        title = self.title + '. ' if hasattr(self, 'title') else 'Unknown Title. '
        if html:
            title = '<i>' + title + '</i>'

        location = self.location + ': ' if hasattr(self, 'location') else ''
        publisher = self.publisher + ', ' if hasattr(self, 'publisher') else ''
        if self.date:
            date = "%i, " % self.date
        else:
            date = ''
        page = 'pp. ' + str(self.page) if hasattr(self, 'page') else ''

        return "%s%s%s%s%s%s" % (author, title, location, publisher, date, page)

    def __repr__(self):
        if hasattr(self, 'title'):
            return "Barbados::Objects::Citation[%s]" % self.title
        else:
            return "Barbados::Objects::Citation[]"

    def serialize(self, serializer):
        serializer.add_property('notes', [ObjectSerializer.serialize(note, serializer.format) for note in self.notes])
        serializer.add_property('title', self.title, even_if_empty=False)
        serializer.add_property('author', self.author, even_if_empty=False)
        serializer.add_property('date', self.date, even_if_empty=False)
        serializer.add_property('publisher', self.publisher, even_if_empty=False)
        serializer.add_property('page', self.page, even_if_empty=False)
        serializer.add_property('href', self.href, even_if_empty=False)
        serializer.add_property('location', self.location, even_if_empty=False)
        serializer.add_property('issue', self.issue, even_if_empty=False)
