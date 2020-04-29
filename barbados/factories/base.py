from barbados.serializers import ObjectSerializer


class BaseFactory:
    @staticmethod
    def obj_to_index(obj, index_class, format='dict'):
        return index_class(meta={'id': obj.slug}, **ObjectSerializer.serialize(obj, format))

    @staticmethod
    def model_to_obj(model):
        raise NotImplementedError

    @staticmethod
    def raw_to_obj(raw):
        raise NotImplementedError
