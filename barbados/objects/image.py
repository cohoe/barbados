from barbados.objects.base import BaseObject


class Image(BaseObject):
    def __init__(self, text, href, credit):
        self.text = text
        self.href = href
        self.credit = credit

    def __repr__(self):
        return "Barbados::Objects::Image[]>"

    def serialize(self, serializer):
        serializer.add_property('text', self.text)
        serializer.add_property('href', self.href)
        serializer.add_property('credit', self.credit)
