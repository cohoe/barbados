from barbados.factories.base import BaseFactory
from barbados.serializers import ObjectSerializer


class SpecResolutionFactory(BaseFactory):
    @staticmethod
    def required_keys():
        pass

    _model = None

    @classmethod
    def model_to_obj(cls, model):
        pass

    @staticmethod
    def raw_to_obj(raw):
        pass

    @classmethod
    def sanitize_raw(cls, raw_input):
        pass

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
        id = "%s::%s::%s" % (obj.inventory_id, obj.cocktail_slug, obj.spec_slug)
        return index_class(meta={'id': id}, **ObjectSerializer.serialize(obj, format))
