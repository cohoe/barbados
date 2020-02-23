from .jsonserializer import JsonSerializer
from .dictserializer import DictSerializer


class SerializerFactory:

    def __init__(self):
        self._creators = {}

    def register_format(self, format, creator):
        self._creators[format] = creator

    def get_serializer(self, format):
        creator = self._creators.get(format)
        if not creator:
            raise ValueError(format)
        return creator()


serializer_factory = SerializerFactory()
serializer_factory.register_format('JSON', JsonSerializer)
serializer_factory.register_format('dict', DictSerializer)


class ObjectSerializer:
    """
    https://realpython.com/factory-method-python/
    """
    @staticmethod
    def serialize(serializable, output_format):
        serializer = serializer_factory.get_serializer(output_format)
        serializable.serialize(serializer)
        return serializer.serialize()
