from barbados.factories.base import BaseFactory
from barbados.objects.drinklist import DrinkList
from barbados.models.drinklist import DrinkListModel
from barbados.validators.drinklistmodel import DrinkListModelValidator
from barbados.indexes.drinklist import DrinkListIndex
from barbados.factories.parser import FactoryParser
from barbados.factories.drinklistitem import DrinkListItemFactory


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
        raw_list = FactoryParser.parse_id(raw_list)
        raw_list = FactoryParser.parse_display_name(raw_list, source_attr='id')
        raw_list = FactoryParser.parse_object_list(raw_list, factory=DrinkListItemFactory, key='items')

        dl = DrinkList(**raw_list)
        return dl
