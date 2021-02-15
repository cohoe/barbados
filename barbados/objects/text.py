import slugify
from datetime import datetime as DateTime
from barbados.objects.base import BaseObject


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


class Text(BaseObject):
    def __init__(self, text, author=None, datetime=None):
        # Disabled autogeneration of datetime values for now.
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


class Timestamp:
    """
    Common class for any stored reference to a timestamp.
    If we were given a timestamp string then we assume it is already formatted
    and we can pass it along. If there was no value then we assume we're generating
    a new timestamp and should return now.
    All UTC All The Time(tm)!
    """
    def __new__(cls, value=None):
        if not value:
            return DateTime.utcnow().isoformat()
        return value
