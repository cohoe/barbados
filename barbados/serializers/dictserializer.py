

class DictSerializer:
    """
    https://realpython.com/factory-method-python/
    """

    format = 'dict'

    def __init__(self):
        self._current_object = {}

    def add_property(self, name, value):
        self._current_object[name] = value

    def serialize(self):
        return self._current_object
