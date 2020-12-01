import copy
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

    @classmethod
    def model_to_obj(cls, model):
        """
        This exists to ensure common functionality with CocktailModel.
        Convert a Model into an Object. There is some SQLAlchemy crap that must
        be removed in order to basically dump the model's dictionary
        into the raw_to_obj() function.
        :param model: barbados.models.BarbadosModel child.
        :return: A barbados.objects.* object instance.
        """
        # Deepcopy is needed to prevent the pop() from affecting
        # the actual model used in-memory by Jamaica.
        # Smells like sqlalchemy.orm.exc.UnmappedInstanceError
        # "but this instance lacks instrumentation"
        try:
            model_dict = copy.deepcopy(model.__dict__)
            model_dict.pop('_sa_instance_state')
        except AttributeError:
            raise KeyError("Object not found")

        return cls.raw_to_obj(model_dict)

    @staticmethod
    def raw_to_obj(raw):
        raise NotImplementedError

    @staticmethod
    def required_keys():
        raise NotImplementedError

    @staticmethod
    def sanitize_raw(raw_input, required_keys):
        """
        Forces the default value of certain required attributes to their expected defaults.
        :param raw_input: Dictionary
        :param required_keys: Dictionary of keys and their data expected data type.
        :return: sanitized raw_input (dict)
        """
        for key in required_keys.keys():
            # If the required key is not in the input, set it to the default.
            if key not in raw_input.keys():
                raw_input[key] = required_keys[key]
            # If the required key should be a list and in the input it is not, force
            # it to an empty list.
            if type(required_keys[key]) is list:
                if raw_input[key] is None:
                    raw_input[key] = required_keys[key]

        return raw_input
