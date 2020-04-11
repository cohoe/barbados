import slugify


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

        return text.title()


class Text:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "Barbados::Object::Text[]"

    def serialize(self, serializer):
        serializer.add_property('text', self.text)


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
