class BaseSerializer:
    """
    https://realpython.com/factory-method-python/
    """

    # @TODO not really sure this works. Non-existent serializers get messed up
    # in the Factory list.
    @property
    def format(self):
        raise NotImplementedError()

    def __init__(self):
        self._current_object = {}

    def add_property(self, name, value, even_if_empty=True):
        """
        :param name:
        :param value:
        :param even_if_empty: Store if false-y ([], {}, None). Don't do this for lists.
        :return:
        """
        if not even_if_empty:
            if not value:
                return
        self._current_object[name] = value

    def serialize(self):
        raise NotImplementedError()
