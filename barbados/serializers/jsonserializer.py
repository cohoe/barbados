import json


class JsonSerializer:
    """
    https://realpython.com/factory-method-python/
    """

    format = 'JSON'

    def __init__(self):
        self._current_object = {}

    def add_property(self, name, value):
        self._current_object[name] = value

    def serialize(self):
        return json.dumps(self._current_object)
