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
