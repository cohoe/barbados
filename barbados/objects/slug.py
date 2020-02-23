import slugify


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
