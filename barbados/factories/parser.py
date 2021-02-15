import datetime
import dateutil.parser
from barbados.exceptions import FactoryException
from barbados.objects.text import DisplayName, Slug
from uuid import UUID, uuid4


class FactoryParser:
    """
    The following functions are all attribute parsers used to properly
    construct the various objects in sub-factories.
    Any object that has its own factory should not be included here since it
    would cause a dependency loop. This library class is intended for more
    primative types.
    """

    @staticmethod
    def parse_id(raw_input, key='id'):
        raw_id = raw_input.get(key)
        if type(raw_id) is UUID:
            id = raw_id
        elif type(raw_id) is str:
            id = UUID(raw_id)
        elif raw_id is None:
            id = uuid4()
        else:
            raise FactoryException("Unable to construct ID")
        raw_input.update({key: id})

        return raw_input

    @staticmethod
    def parse_display_name(raw_input, key='display_name', source_attr='slug'):
        try:
            d = DisplayName(raw_input[key])
        except KeyError:
            d = DisplayName(raw_input.get(source_attr))
        raw_input.update({key: d})
        return raw_input

    @staticmethod
    def parse_date(raw_input, key='date'):
        """
        The single-year method was deprecated and moved to its own field.
        We should only get actual datetime.Date objects.
        :param raw_input:
        :param key:
        :return:
        """
        raw_date = raw_input.get(key)

        if type(raw_date) is datetime.date:
            new_date = raw_date
        elif type(raw_date) is str:
            # In general we trust this because the input serializer should have
            # converted it into a good string for us!
            new_date = dateutil.parser.parse(raw_date).date()
        elif raw_date is None:
            new_date = None
        else:
            raise FactoryException("Bad date value given: %s" % raw_date)

        raw_input.update({key: new_date})
        return raw_input

    @staticmethod
    def parse_object(raw_input, factory, key):
        raw_value = raw_input.get(key)
        obj = factory.raw_to_obj(raw_value)
        raw_input.update({key: obj})
        return raw_input

    @staticmethod
    def parse_object_list(raw_input, factory, key):
        raw_value = raw_input.get(key)
        objs = factory.raw_list_to_obj(raw_value)
        raw_input.update({key: objs})
        return raw_input

    @staticmethod
    def parse_slug(raw_input, key='slug'):
        """
        This is needed to get around having non-slugged values in a majority
        of the Torguga files. I'm not about to go retrofit all of those just to
        satisfy this so in some cases this is going to cause extra computation.
        Fortunately it's pretty simple and reliable.
        Also Tortuga Data Format v3 replaced all names with slugs, but it means that
        the slugs for specs are not accurate. Same problem for ingredients.
        :param raw_input:
        :param key:
        :return:
        """
        raw_value = raw_input.get(key)
        new_value = Slug(raw_value)
        raw_input.update({key: new_value})
        return raw_input

    @staticmethod
    def parse_boolean(raw_input, key):
        """
        Infer a boolean from the value of a given key in the input dict.
        :param raw_input: Dictionary
        :return: Dictionary with corrected bool value
        """
        input_value = raw_input.get(key)

        # Boolean
        if isinstance(input_value, bool):
            pass

        # Integer
        if isinstance(input_value, int):
            raw_input.update({key: bool(input_value)})

        # String
        if isinstance(input_value, str):
            if 'Y' in input_value.upper():
                raw_input.update({key: True})
            else:
                raw_input.update({key: True})

        # None
        if input_value is None:
            raw_input.update({key: False})

        return raw_input
