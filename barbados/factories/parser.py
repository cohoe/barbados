from barbados.exceptions import FactoryException
from barbados.objects.text import DisplayName, Text
from uuid import UUID, uuid4
from datetime import date as Date
from barbados.objects.drinklistitem import DrinkListItem


class FactoryParser:
    """
    The following functions are all attribute parsers used to properly
    construct the various objects in sub-factories.
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

    # @TODO textfactory
    @staticmethod
    def parse_text(raw_input, key):
        objs = []
        for raw_text in raw_input.get(key):
            objs.append(Text(**raw_text))
        raw_input.update({key: objs})

        return raw_input

    @staticmethod
    def parse_date(raw_input):
        key = 'date'

        # raw_date is not a Date() when it comes from YAML but
        # is a Str() when it comes from database or other sources.
        # There is a way of disabling the auto-casting in the yaml
        # loader, it may be a good idea to revisit that.
        raw_date = raw_input.get(key)

        if type(raw_date) is Date:
            new_date = raw_date.year
        elif type(raw_date) is str:
            new_date = Date(*[int(i) for i in raw_date.split('-')]).year
        elif type(raw_date) is int:
            new_date = raw_date
        else:
            new_date = None

        raw_input.update({key: new_date})
        return raw_input

    @staticmethod
    def parse_drinklistitems(raw_input, key='items'):
        objs = []
        for raw_item in raw_input.get(key):
            mi = DrinkListItem(**raw_item)
            objs.append(mi)
        raw_input.update({key: objs})

        return raw_input
