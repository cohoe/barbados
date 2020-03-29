from .baseserializer import BaseSerializer


class DictSerializer(BaseSerializer):
    """
    https://realpython.com/factory-method-python/
    """

    format = 'dict'

    def serialize(self):
        return self._current_object
