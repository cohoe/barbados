class BaseSerializer:
    """
    Base serializer class that all serializers must implement.
    """

    @property
    def format(self):
        """
        Format key (String)
        :return: String of the format key.
        """
        raise NotImplementedError

    def __init__(self):
        """
        Internal state should be kept private.
        """
        self._current_object = {}

    def add_property(self, key, value, even_if_empty=True):
        """
        :param key: Key of the parameter you want to add to the serialized object.
        :param value: Value of the parameter you want to add to the serialized object.
        :param even_if_empty: Store if false-y ([], {}, None). Don't do this for lists.
        :return: None
        """
        if not even_if_empty:
            if not value:
                return
        self._current_object[key] = value

    def serialize(self):
        """
        Method to actually generate the serialized object.
        This is what actually gets called in the objects.
        :return: Various.
        """
        raise NotImplementedError
