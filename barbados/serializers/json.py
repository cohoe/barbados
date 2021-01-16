import json
from barbados.serializers.base import BaseSerializer


class JsonSerializer(BaseSerializer):
    """
    Serialize an object into a JSON blob all essential data.
    """
    format = 'JSON'

    def serialize(self):
        return json.dumps(self._current_object)
