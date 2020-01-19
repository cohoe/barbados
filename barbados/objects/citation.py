

class Citation:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

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
        if hasattr(self, 'date'):
            if isinstance(self.date, int):
                date = str(self.date)
            else:
                date = self.date.strftime('%Y')

            date += ', '
        else:
            date = ''
        page = 'pp. ' + str(self.page) if hasattr(self, 'page') else ''

        return "%s%s%s%s%s%s" % (author, title, location, publisher, date, page)

    def __repr__(self):
        if hasattr(self, 'title'):
            return "<Object:Citation::title=%s>" % self.title
        else:
            return "<Object:Citation>"

    def serialize(self):
        ser = {}
        keys = ['title', 'author', 'date', 'publisher', 'page']

        for key in keys:
            if hasattr(self, key):
                ser[key] = getattr(self, key)

        if 'date' in ser.keys():
            ser['date'] = str(ser['date'])

        return ser