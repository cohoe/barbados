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

    def add_property(self, name, value, even_if_none=True):
        if not even_if_none:
            if not value:
                return
        self._current_object[name] = value

    def serialize(self):
        raise NotImplementedError()
