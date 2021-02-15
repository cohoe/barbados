import datetime
import dateutil.parser
from barbados.exceptions import FactoryException
from barbados.objects.text import DisplayName
from uuid import UUID, uuid4
from barbados.objects.drinklistitem import DrinkListItem


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
    # @TODO technically this should be a factory....
    def parse_drinklistitems(raw_input, key='items'):
        objs = []
        for raw_item in raw_input.get(key):
            mi = DrinkListItem(**raw_item)
            objs.append(mi)
        raw_input.update({key: objs})

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
