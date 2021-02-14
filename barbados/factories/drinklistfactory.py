from barbados.factories.base import BaseFactory
from barbados.objects.drinklist import DrinkList
from barbados.objects.drinklistitem import DrinkListItem
from barbados.models.drinklist import DrinkListModel
from barbados.validators.drinklistmodel import DrinkListModelValidator
from barbados.indexes.drinklist import DrinkListIndex


class DrinkListFactory(BaseFactory):
    _model = DrinkListModel
    _validator = DrinkListModelValidator
    _index = DrinkListIndex

    required_keys = {
        'items': list(),
    }

    unwanted_keys = [
        'slug'  # This was deprecated
    ]

    @classmethod
    def raw_to_obj(cls, raw):
        raw_list = cls.sanitize_raw(raw, required_keys=cls.required_keys,
                                    unwanted_keys=cls.unwanted_keys)

        # Parse
        raw_list = cls._parse_id(raw_list)
        raw_list = cls._parse_display_name(raw_list, source_attr='id')
        raw_list = cls._parse_items(raw_list)

        dl = DrinkList(**raw_list)
        return dl

    @staticmethod
    def _parse_items(raw_input):
        key = 'items'

        objs = []
        for raw_item in raw_input.get(key):
            mi = DrinkListItem(**raw_item)
            objs.append(mi)
        raw_input.update({key: objs})

        return raw_input
