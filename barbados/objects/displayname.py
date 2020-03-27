class DisplayName:
    """
    This class exists to provide a common place for generating display name text
    based on consistent rules.
    """

    def __new__(cls, text):
        # @TODO do anything more fancy
        return text.title()
