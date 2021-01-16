from barbados.serializers.json import JsonSerializer
from barbados.serializers.dict import DictSerializer


class SerializerFactory:
    """
    This factory controls the loading and management of all Serializers.
    Loosly based on https://realpython.com/factory-method-python/
    """
    def __init__(self):
        """
        The internal state tracking is kept private intentionally.
        """
        self._serializers = {}

    def register_format(self, serializer):
        """
        Register a new serializer with the
        :param serializer: barbados.serializers.base.BaseSerializer child class.
        :return: None
        """
        self._serializers[serializer.format] = serializer

    def get_serializer(self, format):
        """
        Lookup a serializer based on a given format.
        :param format: String key representing the format you want to serialize to.
        :return: barbados.serializers.base.BaseSerializer instance.
        :raises ValueError: We don't have a serializer for that format.
        """
        serializer = self._serializers.get(format)
        if not serializer:
            raise ValueError(format)
        return serializer()


serializer_factory = SerializerFactory()
serializer_factory.register_format(JsonSerializer)
serializer_factory.register_format(DictSerializer)


class ObjectSerializer:
    """
    Generic object serializer class that provides a common way to serialize
    any supported object to any format.
    """
    @staticmethod
    def serialize(serializable, output_format):
        """
        Take an object and serialize it to the format specified.
        :param serializable: barbados.objects.* that supports serialization.
        :param output_format: String key of the format you want to serialize to.
        :return: Output of the serialization of the object.
        """
        serializer = serializer_factory.get_serializer(output_format)
        serializable.serialize(serializer)
        return serializer.serialize()
