import slugify
from datetime import datetime as DateTime


class DisplayName:
    """
    This class exists to provide a common place for generating display name text
    based on consistent rules.
    """

    # Custom replacements
    replacements = [
        ["-", ' ']
    ]

    def __new__(cls, text):
        for replacement in cls.replacements:
            text = text.replace(replacement[0], replacement[1])

        if text.isupper():
            return text

        return text.title()


class Text:
    def __init__(self, text, author=None, datetime=None):
        if not datetime:
            datetime = DateTime.utcnow().isoformat()

        self.text = text
        self.author = author
        self.datetime = datetime

    def __repr__(self):
        return "Barbados::Objects::Text[]"

    def serialize(self, serializer):
        serializer.add_property('text', self.text)
        serializer.add_property('author', self.author)
        serializer.add_property('datetime', self.datetime)


class Slug:
    """
    This class exists to provide a common place for slugifying text
    based on consistent rules.
    """

    # Custom replacements
    replacements = [
        ["'", '']
    ]

    def __new__(cls, text):
        return slugify.slugify(text=text, replacements=cls.replacements)
