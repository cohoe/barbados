from barbados.serializers import ObjectSerializer


class BaseFactory:
    @staticmethod
    def obj_to_index(obj, index_class, format='dict'):
        """
        Serialize an object into a standard form suitable
        for indexing.
        :param obj: Serializable object.
        :param index_class: The ElasticSearch DSL class representing the intended index.
        :param format: Format of the data to pass to the serializer.
        :return: Instance of the Index class.
        """
        return index_class(meta={'id': obj.slug}, **ObjectSerializer.serialize(obj, format))

    @staticmethod
    def model_to_obj(model):
        raise NotImplementedError

    @staticmethod
    def raw_to_obj(raw):
        raise NotImplementedError