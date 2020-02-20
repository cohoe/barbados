import json


class JsonSerializer:
    """
    https://realpython.com/factory-method-python/
    """
    def __init__(self):
        self._current_object = {}

    def add_property(self, name, value):
        self._current_object[name] = value

    def to_str(self):
        return json.dumps(self._current_object)
