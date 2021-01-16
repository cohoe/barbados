from barbados.serializers.base import BaseSerializer


class DictSerializer(BaseSerializer):
    """
    Serialize an object into a dictionary containing all essential data.
    """
    format = 'dict'

    def serialize(self):
        return self._current_object
