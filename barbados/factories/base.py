from barbados.serializers import ObjectSerializer


class BaseFactory:
    @staticmethod
    def obj_to_index(obj, index_class, format='dict'):
        return index_class(meta={'id': obj.slug}, **ObjectSerializer.serialize(obj, format))
