import json
from .baseserializer import BaseSerializer


class JsonSerializer(BaseSerializer):
    """
    https://realpython.com/factory-method-python/
    """

    format = 'JSON'

    def serialize(self):
        return json.dumps(self._current_object)
