from .jsonserializer import JsonSerializer


class SerializerFactory:

    def __init__(self):
        self._creators = {}

    def register_format(self, format, creator):
        print("Registered %s" % format)
        self._creators[format] = creator

    def get_serializer(self, format):
        creator = self._creators.get(format)
        if not creator:
            raise ValueError(format)
        return creator()


serializer_factory = SerializerFactory()
serializer_factory.register_format('JSON', JsonSerializer)


class Serializer:
    """
    https://realpython.com/factory-method-python/
    """
    @staticmethod
    def serialize(serializable, format):
        serializer = serializer_factory.get_serializer(format)
        serializable.serialize(serializer)
        return serializer.to_str()
